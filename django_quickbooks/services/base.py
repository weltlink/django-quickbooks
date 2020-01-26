from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.utils import get_xml_meta_info, xml_setter


class Service:
    ref_fields = []
    add_fields = []
    complex_fields = []
    mod_fields = []

    def _prepare_request(self, req_body):
        xml = xml_setter('QBXMLMsgsRq', req_body, onError='stopOnError')
        xml = xml_setter('QBXML', xml)
        xml = get_xml_meta_info() + xml
        return xml

    def _add(self, resource, object):
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_ADD + 'Rq', object.as_xml(
            opp_type=QUICKBOOKS_ENUMS.OPP_ADD, ref_fields=self.ref_fields, change_fields=self.add_fields, complex_fields=self.complex_fields))
        return self._prepare_request(xml)

    def _update(self, resource, object):
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_MOD + 'Rq', object.as_xml(
            opp_type=QUICKBOOKS_ENUMS.OPP_MOD, ref_fields=self.ref_fields, change_fields=self.mod_fields, complex_fields=self.complex_fields))
        return self._prepare_request(xml)

    def _void(self, resource, object):
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_VOID + 'Rq', object.as_xml(opp_type=QUICKBOOKS_ENUMS.OPP_VOID))
        return self._prepare_request(xml)

    def _delete(self, resource, object):
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_DEL + 'Rq', object.as_xml(opp_type=QUICKBOOKS_ENUMS.OPP_DEL))
        return self._prepare_request(xml)

    def _all(self, resource):
        xml = xml_setter('MaxReturned', 100)
        xml = xml_setter(resource + QUICKBOOKS_ENUMS.OPP_QR + 'Rq', xml, metaData='NoMetaData', iterator='Start')
        return self._prepare_request(xml)

    def _find_by_id(self, resource, id, field_name='ListID'):
        xml = xml_setter(field_name, id)
        xml = xml_setter(resource + QUICKBOOKS_ENUMS.OPP_QR + 'Rq', xml, metaData='NoMetaData')
        return self._prepare_request(xml)

    def _find_by_full_name(self, resource, full_name):
        xml = xml_setter('FullName', full_name)
        xml = xml_setter(resource + QUICKBOOKS_ENUMS.OPP_QR + 'Rq', xml, metaData='NoMetaData')
        return self._prepare_request(xml)
