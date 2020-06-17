from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class ServiceOfItemService(Service):
    ref_fields = ['Account']
    add_fields = []
    mod_fields = []
    complex_fields = ['SalesOrPurchase']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE, id)

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE, full_name)
