from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import ItemService
from django_quickbooks.objects.invoice import ItemService as QBDItemService
from django_quickbooks.processors import ResponseProcessor
from django_quickbooks.processors.base import ResponseProcessorMixin


class ItemServiceAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = ItemService
    obj_class = QBDItemService

    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        for item_service_ret in list(self._response_body):
            item_service = self.obj_class.from_lxml(item_service_ret)
            local_item_service = None
            if item_service.ListID:
                local_item_service = self.find_by_list_id(item_service.ListID, realm.id)
            if not local_item_service and item_service.Name:
                local_item_service = self.find_by_name(item_service.Name, realm.id)

            if local_item_service:
                self.update(local_item_service, item_service)
            else:
                self.create(item_service, realm.id)
        return True


class ItemServiceModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = ItemService
    obj_class = QBDItemService

    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for item_service_ret in list(self._response_body):
            item_service = self.obj_class.from_lxml(item_service_ret)
            local_item_service = None
            if item_service.ListID:
                local_item_service = self.find_by_list_id(item_service.ListID, realm.id)
            elif not local_item_service and item_service.Name:
                local_item_service = self.find_by_name(item_service.Name, realm.id)

            if local_item_service:
                self.update(local_item_service, item_service)
        return True


class ItemServiceQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = ItemService
    obj_class = QBDItemService

    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        for item_service_ret in list(self._response_body):
            item_service = self.obj_class.from_lxml(item_service_ret)
            local_item_service = None
            if item_service.ListID:
                local_item_service = self.find_by_list_id(item_service.ListID, realm.id)
            if not local_item_service and item_service.Name:
                local_item_service = self.find_by_name(item_service.Name, realm.id)

            if local_item_service:
                self.update(local_item_service, item_service)
            else:
                self.create(item_service, realm.id)

        return True
