from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class BillAddress(BaseObject):
    fields = dict(
        Addr1=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Addr2=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Addr3=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Addr4=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Addr5=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        City=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        State=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        PostalCode=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Country=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )


class ItemService(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        Name=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Parent=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.item_service import ServiceOfItemService
        return ServiceOfItemService


class InvoiceItem(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        FullName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )


class InvoiceLine(BaseObject):
    fields = dict(
        TxnLineID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        Item=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Quantity=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
        Rate=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
    )


class Invoice(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Customer=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        BillAddress=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        IsPending=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        DueDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Memo=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        InvoiceLine=dict(validator=dict(type=SchemeValidator.LISTTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.invoice import InvoiceService
        return InvoiceService
