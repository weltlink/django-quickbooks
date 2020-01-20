from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class InvoiceService(Service):
    ref_fields = ['Customer', 'Item']
    add_fields = ['InvoiceLine']
    complex_fields = ['BillAddress']
    mod_fields = ['InvoiceLine']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_INVOICE, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_INVOICE, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_INVOICE)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_INVOICE, id)

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_INVOICE, full_name)
