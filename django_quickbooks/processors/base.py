from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from lxml import etree

from django_quickbooks import QBXML_RESPONSE_STATUS_CODES
from django_quickbooks.decorators import realm_connection
from django_quickbooks.exceptions import QBXMLParseError, QBXMLStatusError


class ResponseProcessor:
    resource = None
    op_type = None
    obj_class = None

    def __init__(self, response, hresult, message):
        self._actual_response_type = None
        self._response_body = None
        self._response = response
        self.hresult = hresult
        self.message = message
        self._process()

    def _process(self):
        if self.hresult:
            raise QBXMLStatusError(self.message)
        qbxml_root = etree.fromstring(self._response)
        if qbxml_root.tag != 'QBXML':
            raise QBXMLParseError('QBXML tag not found')
        if len(qbxml_root) != 1:
            raise QBXMLParseError('QBXML has more or less than 1 child')
        qbxml_msg_rs = qbxml_root[0]
        if qbxml_msg_rs.tag != 'QBXMLMsgsRs':
            raise QBXMLParseError('QBXMLMsgsRs tag not found')
        if len(qbxml_msg_rs) != 1:
            raise QBXMLParseError('QBXMLMsgsRs has more or less than 1 child')
        response_body_root = qbxml_msg_rs[0]
        if 'statusCode' not in response_body_root.attrib:
            raise QBXMLParseError('statusCode is not found in %s' % response_body_root.tag)
        self._actual_response_type = response_body_root.tag
        self._response_body = response_body_root
        self.status_code = response_body_root.attrib['statusCode']
        self.status_message = response_body_root.attrib.get('statusMessage', '')

    def is_valid(self) -> bool:
        return '%s%sRs' % (self.resource, self.op_type) == self._actual_response_type

    @method_decorator(realm_connection())
    def process(self, realm):
        assert self.resource, 'resource attribute is not defined during class definition ' \
                              'of %s' % self.__class__.__name__
        assert self.op_type, 'op_type attribute is not defined during class definition ' \
                             'of %s' % self.__class__.__name__
        if not self.is_valid():
            return False

        if self.status_code != QBXML_RESPONSE_STATUS_CODES.OK:
            raise QBXMLStatusError(self.status_message)

        return True


class ResponseProcessorMixin:
    local_model_class = None

    def update(self, local_obj, obj):
        if local_obj.qbd_object_version != obj.EditSequence:
            local_obj.name = obj.Name
            local_obj.qbd_object_id = obj.ListID
            local_obj.qbd_object_updated_at = timezone.now() + timezone.timedelta(minutes=1)
            local_obj.qbd_object_version = obj.EditSequence
            local_obj.save()

    def find_by_list_id(self, list_id):
        try:
            return self.local_model_class.objects.get(qbd_object_id=list_id)
        except ObjectDoesNotExist:
            return None

    def find_by_name(self, name, field_name='name'):
        try:
            return self.local_model_class.objects.get(**{field_name: name})
        except ObjectDoesNotExist:
            return None

    def create(self, obj):
        customer = self.local_model_class.from_qbd_obj(obj)
        customer.save()
