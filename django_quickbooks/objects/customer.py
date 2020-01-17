from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Customer(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Name=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
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
