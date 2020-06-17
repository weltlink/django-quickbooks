from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import ServiceAccount
from django_quickbooks.objects.account import Account
from django_quickbooks.processors import ResponseProcessor
from django_quickbooks.processors.base import ResponseProcessorMixin


class ServiceAccountQueryProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = ServiceAccount
    obj_class = Account

    resource = QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT
    op_type = QUICKBOOKS_ENUMS.OPP_QR

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        for account_ret in list(self._response_body):
            account = self.obj_class.from_lxml(account_ret)
            local_account = None
            if account.ListID:
                local_account = self.find_by_list_id(account.ListID, realm.id)
            if not local_account and account.Name:
                local_account = self.find_by_name(account.Name, realm.id)

            if local_account:
                self.update(local_account, account)
            else:
                self.create(account, realm.id)

        return True
