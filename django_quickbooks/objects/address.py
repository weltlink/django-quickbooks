from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Address(BaseObject):
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
        Note=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )


class BillAddress(Address):
    pass


class ShipAddress(Address):
    pass
