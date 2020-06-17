from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class AccountService(Service):
    ref_fields = []
    add_fields = []
    complex_fields = []
    mod_fields = []

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT, id, field_name='ListID')

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT, full_name)


class SalesOrPurchaseService(Service):
    ref_fields = ['Account']
    add_fields = []
    complex_fields = []
    mod_fields = []
