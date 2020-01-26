from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Customer(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.ESTYPE)),
        Name=dict(required=False, validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        CompanyName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        BillAddress=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        ShipAddress=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Phone=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        AltPhone=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Fax=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Email=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Contact=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        AltContact=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )

    def __init__(self, Name=None, IsActive=None, **kwargs):
        if Name:
            self.Name = Name

        if IsActive:
            self.IsActive = IsActive

        super().__init__(**kwargs)

    @staticmethod
    def get_service():
        from django_quickbooks.services.customer import CustomerService
        return CustomerService
