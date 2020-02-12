from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.invoice import Invoice
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalInvoice = qbwc_settings.LOCAL_MODEL_CLASSES['Invoice']


class InvoiceAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for invoice_ret in list(self._response_body):
            invoice = self.obj_class.from_lxml(invoice_ret)
            local_invoice = None

            if invoice.TxnID:
                local_invoice = self.find_by_id(invoice.Memo)

            if local_invoice:
                self.update(local_invoice, invoice)

        return True

    def find_by_id(self, id):
        try:
            return self.local_model_class.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def update(self, local_obj, obj):
        local_obj.qbd_object_id = obj.TxnID
        local_obj.qbd_object_updated_at = timezone.now() + timezone.timedelta(minutes=1)
        local_obj.qbd_object_version = obj.EditSequence
        local_obj.save()


class InvoiceModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class InvoiceQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
