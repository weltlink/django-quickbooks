from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Account(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.ESTYPE)),
        Name=dict(required=False, validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        Parent=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        AccountType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        AccountNumber=dict(validator=dict(type=SchemeValidator.INTTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.account import AccountService
        return AccountService


class SalesOrPurchase(BaseObject):
    fields = dict(
        Account=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )
