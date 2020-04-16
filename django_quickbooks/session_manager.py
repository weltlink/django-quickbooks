import logging

logger = logging.getLogger('django')

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from lxml import etree

from django_quickbooks import get_realm_session_model, get_realm_model, get_qbd_task_model
from django_quickbooks.core.session_manager import BaseSessionManager
from django_quickbooks.decorators import realm_connection
from django_quickbooks.exceptions import QBXMLParseError, QBXMLStatusError, QbException

Realm = get_realm_model()
RealmSession = get_realm_session_model()
QBDTask = get_qbd_task_model()


class SessionManager(BaseSessionManager):

    def __init__(self, queue_manager, request_queue_prefix=None, iterating_request_queue_prefix=None, **kwargs):
        self.queue_manager = queue_manager

        if request_queue_prefix is None:
            request_queue_prefix = 'requests:realms:'
        if iterating_request_queue_prefix is None:
            iterating_request_queue_prefix = 'iterating_requests:tickets:'

        self.request_queue_prefix = request_queue_prefix
        self.iterating_request_queue_prefix = iterating_request_queue_prefix
        super().__init__(**kwargs)

    def authenticate(self, username, password):
        return Realm.objects.find(username, password)

    def create_session(self, realm):
        realm_session = RealmSession.objects.create(realm=realm)
        return str(realm_session.id)

    def in_session(self, realm):
        return RealmSession.objects.is_active(realm)

    @method_decorator(realm_connection())
    def add_new_requests(self, realm=None):
        queryset = QBDTask.objects.filter(realm=realm).order_by('created_at')
        for qb_task in queryset:
            try:
                request = qb_task.get_request()
                self.put_request(request, realm)
            except QbException as exc:
                logger.error(exc.detail)
            except ObjectDoesNotExist as e:
                logger.error(e)

        queryset.delete()

    def new_requests_count(self, realm):
        queue_name = '%s:%s' % (self.request_queue_prefix, realm.id)
        return self.queue_manager.get_message_count(queue_name)

    def process_response(self, ticket, response, hresult, message):
        from django_quickbooks import get_processors
        realm = self.get_realm(ticket)
        processors = get_processors()
        for processor in processors:
            try:
                processed = processor(response, hresult, message).process(realm)
                if processed:
                    break

            except QBXMLParseError as exc:
                logger.error(exc.detail)
                return -1
            except QBXMLStatusError as exc:
                logger.error(exc.detail)
                return -1

        self._continue_iterative_response(ticket, response)

        requests_count = self.new_requests_count(realm)
        requests_count = requests_count if requests_count <= 98 else 98

        if not requests_count:
            queue_name = '%s:%s' % (self.request_queue_prefix, realm.id)
            self.queue_manager.purge(queue_name)

        return int(100 / (requests_count + 1))

    def get_realm(self, ticket):
        return RealmSession.objects.get(id=ticket).realm

    def put_request(self, request, realm):
        queue_name = '%s:%s' % (self.request_queue_prefix, realm.id)
        self.queue_manager.publish_message(request, queue_name)

    def get_request(self, realm):
        queue_name = '%s:%s' % (self.request_queue_prefix, realm.id)
        return self.queue_manager.get_message(queue_name)

    def check_iterating_request(self, request, ticket):
        if self.is_iterating_request(request):
            self._put_iterating_request(request, ticket)

    def is_iterating_request(self, request):
        root = etree.fromstring(request)
        return root.xpath('boolean(//@iterator)')

    def close_session(self, realm):
        realm_session = RealmSession.objects.get_by(realm)
        requests_queue_name = '%s:%s' % (self.request_queue_prefix, realm.id)
        iterating_requests_queue_name = '%s:%s' % (self.iterating_request_queue_prefix, realm_session.id)

        self.queue_manager.delete(requests_queue_name)
        self.queue_manager.delete(iterating_requests_queue_name)

        realm_session.close()

    def _get_iterating_request(self, ticket):
        queue_name = '%s:%s' % (self.iterating_request_queue_prefix, ticket)
        return self.queue_manager.get_message(queue_name)

    def _put_iterating_request(self, request, ticket):
        queue_name = '%s:%s' % (self.iterating_request_queue_prefix, ticket)
        self.queue_manager.publish_message(request, queue_name, delete_queue=True)

    def _continue_iterative_response(self, ticket, response):
        root = etree.fromstring(bytes(str(response), encoding='utf-8'))
        isIterator = root.xpath('boolean(//@iteratorID)')
        if isIterator:
            reqXML = self._get_iterating_request(ticket)
            reqroot = etree.fromstring(reqXML)
            iteratorRemainingCount = int(root.xpath('string(//@iteratorRemainingCount)'))
            iteratorID = root.xpath('string(//@iteratorID)')
            if iteratorRemainingCount:
                iteratornode = reqroot.xpath('//*[@iterator]')
                iteratornode[0].set('iterator', 'Continue')
                request_id_path = reqroot.xpath('//@requestID')
                if request_id_path:
                    requestID = int(request_id_path[0])
                    iteratornode[0].set('requestID', str(requestID + 1))
                iteratornode[0].set('iteratorID', iteratorID)
                ntree = etree.ElementTree(reqroot)
                nextreqXML = etree.tostring(ntree, xml_declaration=True, encoding='UTF-8')
                self.put_request(nextreqXML, self.get_realm(ticket))
