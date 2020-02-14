import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from lxml import etree

from django_quickbooks import get_realm_session_model, get_realm_model, get_qbd_task_model
from django_quickbooks.core.session_manager import BaseSessionManager
from django_quickbooks.decorators import realm_connection
from django_quickbooks.exceptions import QBXMLParseError, QBXMLStatusError, QbException
from django_quickbooks.queue_manager import RabbitMQManager

Realm = get_realm_model()
RealmSession = get_realm_session_model()
QBDTask = get_qbd_task_model()


def _get_realm(ticket):
    return RealmSession.objects.get(id=ticket).realm


class SessionManager(BaseSessionManager, RabbitMQManager):

    def authenticate(self, username, password):
        return Realm.objects.find(username, password)

    def set_ticket(self, realm):
        return str(RealmSession.objects.create(realm=realm).id)

    def in_session(self, realm):
        return RealmSession.objects.is_active(realm)

    @method_decorator(realm_connection())
    def add_new_jobs(self, realm=None):
        queryset = QBDTask.objects.filter(realm=realm).order_by('created_at')
        for qb_task in queryset:
            try:
                self.publish_message(qb_task.get_request(), str(realm.id))
            except QbException as exc:
                logger = logging.getLogger('django.request')
                logger.error(exc.detail)
            except ObjectDoesNotExist:
                pass

        queryset.delete()

    def new_jobs(self, realm):
        return self.get_queue_message_count(str(realm.id))

    def process_response(self, ticket, response, hresult, message):
        from django_quickbooks import get_processors
        realm = _get_realm(ticket)
        processors = get_processors()
        for processor in processors:
            try:
                processed = processor(response, hresult, message).process(realm)
                if processed:
                    break

            except QBXMLParseError as exc:
                logger = logging.getLogger('django.request')
                logger.error(exc.detail)
                return -1
            except QBXMLStatusError as exc:
                logger = logging.getLogger('django.request')
                logger.error(exc.detail)
                return -1

        self._continue_iterative_response(ticket, response)

        jobs_count = self.new_jobs(realm)
        jobs_count = jobs_count if jobs_count <= 98 else 98

        if not jobs_count:
            self.purge_queue(str(realm.id))

        return int(100 / (jobs_count + 1))

    def get_request(self, ticket):
        request = self.get_message(_get_realm(ticket).id)
        if self.is_iterating_request(request):
            self._set_iterative_request(ticket, request)
        return request

    def is_iterating_request(self, request):
        root = etree.fromstring(bytes(str(request), encoding='utf-8'))
        isIterator = root.xpath('boolean(//@iterator)')
        return isIterator

    def clear_ticket(self, ticket):
        RealmSession.objects.close_session(_get_realm(ticket))
        self.delete_queue(ticket)
        return ticket

    def _get_iterative_request(self, ticket):
        return self.get_message(ticket)

    def _set_iterative_request(self, ticket, request):
        self.publish_message(request, ticket, delete_queue=True)

    def _continue_iterative_response(self, ticket, response):
        root = etree.fromstring(bytes(str(response), encoding='utf-8'))
        isIterator = root.xpath('boolean(//@iteratorID)')
        if isIterator:
            reqXML = self._get_iterative_request(ticket)
            reqroot = etree.fromstring(bytes(str(reqXML), encoding='utf-8'))
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
                self.publish_message(nextreqXML, _get_realm(ticket).id)
