from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import Customer
from django_quickbooks.objects.customer import Customer as QBDCustomer
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin


class CustomerQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = Customer
    obj_class = QBDCustomer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID, realm.id)
            if not local_customer and customer.FullName:
                local_customer = self.find_by_name(customer.FullName, realm.id, field_name='full_name')

            if local_customer:
                self.update(local_customer, customer)
            else:
                self.create(customer, realm.id)
        return True

    def update(self, local_obj, obj):
        if local_obj.edit_sequence != obj.EditSequence:
            local_obj.name = obj.Name
            local_obj.full_name = obj.FullName
            local_obj.list_id = obj.ListID
            local_obj.edit_sequence = obj.EditSequence
            local_obj.time_created = obj.TimeCreated
            local_obj.time_modified = obj.TimeModified
            local_obj.save(
                update_fields=['name', 'full_name', 'list_id', 'edit_sequence', 'time_created', 'time_modified'])


class CustomerAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = Customer
    obj_class = QBDCustomer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.FullName:
                local_customer = self.find_by_name(customer.FullName, realm.id, field_name='full_name')

            if local_customer:
                self.update(local_customer, customer)
        return True

    def update(self, local_obj, obj):
        if local_obj.edit_sequence != obj.EditSequence:
            local_obj.list_id = obj.ListID
            local_obj.edit_sequence = obj.EditSequence
            local_obj.time_created = obj.TimeCreated
            local_obj.time_modified = obj.TimeModified
            local_obj.save(update_fields=['list_id', 'edit_sequence', 'time_created', 'time_modified'])


class CustomerModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = Customer
    obj_class = QBDCustomer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID, realm.id)
            elif not local_customer and customer.FullName:
                local_customer = self.find_by_name(customer.FullName, realm.id, field_name='full_name')

            if local_customer:
                self.update(local_customer, customer)
        return True

    def update(self, local_obj, obj):
        if local_obj.edit_sequence != obj.EditSequence:
            local_obj.name = obj.Name
            local_obj.full_name = obj.FullName
            local_obj.list_id = obj.ListID
            local_obj.edit_sequence = obj.EditSequence
            local_obj.time_created = obj.TimeCreated
            local_obj.time_modified = obj.TimeModified
            local_obj.save(
                update_fields=['name', 'full_name', 'list_id', 'edit_sequence', 'time_created', 'time_modified'])
