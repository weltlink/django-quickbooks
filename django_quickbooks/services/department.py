from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class DepartmentService(Service):

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT, id)

    def find_by_department_name(self, department_name):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT, department_name, field_name='DepartmentName')

    def find_by_department_code(self, department_code):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_DEPARTMENT, department_code, field_name='DepartmentCode')
