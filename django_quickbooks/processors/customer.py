from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.customer import Customer
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalCustomer = qbwc_settings.LOCAL_MODEL_CLASSES['Customer']


class CustomerQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID)
            elif not local_customer and customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
            else:
                self.create(customer)
        return True


class CustomerAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
        return True


class CustomerModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID)
            elif not local_customer and customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
        return True
