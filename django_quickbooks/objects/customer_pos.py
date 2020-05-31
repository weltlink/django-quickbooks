from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Customer(BaseObject):
    fields = dict(
        CompanyName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        # CustomerDiscType may have one of the following values: None,PriceLevel,Percentage
        CustomerDiscType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EMail=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        FirstName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        LastName=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE)),
        Phone=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Notes=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Phone2=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        # PriceLevelNumber may have one of the following values: 1,2,3,4
        PriceLevelNumber=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Salutation=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        BillAddress=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        ShipAddress=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
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
