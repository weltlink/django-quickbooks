from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Department(BaseObject):
    fields = dict(
        DefaultMarginPercent=dict(validator=dict(type=SchemeValidator.INTTYPE)),
        DefaultMarkupPercent=dict(validator=dict(type=SchemeValidator.INTTYPE)),
        DepartmentCode=dict(required=True, validator=dict(type=SchemeValidator.STRTYPE, max_length=3)),
        DepartmentName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TaxCode=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )

    def __init__(self, Name=None, **kwargs):
        if Name:
            self.DepartmentName = Name

        super().__init__(**kwargs)

    @staticmethod
    def get_service():
        from django_quickbooks.services.department import DepartmentService
        return DepartmentService
