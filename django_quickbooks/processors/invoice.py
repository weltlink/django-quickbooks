from django.core.exceptions import ObjectDoesNotExist

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import Invoice
from django_quickbooks.objects.invoice import Invoice as QBDInvoice
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin


class InvoiceAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = Invoice
    obj_class = QBDInvoice

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
        local_obj.list_id = obj.TxnID
        local_obj.edit_sequence = obj.EditSequence
        local_obj.save()


class InvoiceModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = Invoice
    obj_class = QBDInvoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class InvoiceQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = Invoice
    obj_class = QBDInvoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
