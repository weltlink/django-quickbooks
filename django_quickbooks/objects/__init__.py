from django.utils.module_loading import import_string


def import_object_cls(resource_name):
    try:
        return import_string('%s.%s' % (__package__, resource_name))
    except ImportError:
        return None


from django_quickbooks.objects.customer import \
    Customer

from django_quickbooks.objects.address import \
    BillAddress, \
    ShipAddress

from django_quickbooks.objects.invoice import \
    ItemService, \
    InvoiceLine, \
    Invoice
