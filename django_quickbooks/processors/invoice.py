from django.core.exceptions import ObjectDoesNotExist

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import Invoice
from django_quickbooks.objects.invoice import Txn as QBDTxn, Invoice as QBDInvoice
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

                if not local_invoice:
                    local_invoice = self.find_by_id(invoice.TxnID, field_name='list_id')

            if local_invoice:
                self.update(local_invoice, invoice)

        return True

    def find_by_id(self, id, field_name='id'):
        try:
            return self.local_model_class.objects.get(**{field_name: id})
        except ObjectDoesNotExist:
            return None

    def update(self, local_obj, obj):
        local_obj.list_id = obj.TxnID
        local_obj.edit_sequence = obj.EditSequence
        local_obj.time_created = obj.TimeCreated
        local_obj.time_modified = obj.TimeModified
        local_obj.txn_date = obj.TxnDate
        local_obj.save(update_fields=['list_id', 'edit_sequence', 'time_created', 'time_modified', 'txn_date'])

        for invoice_line in obj.InvoiceLine:
            local_obj.invoice_lines.filter(id=invoice_line.Desc).update(txn_line_id=invoice_line.TxnLineID)


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

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        for invoice_ret in list(self._response_body):
            invoice = self.obj_class.from_lxml(invoice_ret)
            local_invoice = None

            if invoice.TxnID:
                local_invoice = self.find_by_list_id(invoice.TxnID, realm.id)

            if not local_invoice:
                self.create(invoice, realm.id)

        return True


class InvoiceVoidResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = Invoice
    obj_class = QBDTxn
    resource = QUICKBOOKS_ENUMS.RESOURCE_TXN
    op_type = QUICKBOOKS_ENUMS.OPP_VOID

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        txn = self.obj_class.from_lxml(self._response_body)
        local_invoice = None

        if txn.TxnID:
            local_invoice = self.find_by_list_id(txn.TxnID, realm.id)

        if local_invoice:
            local_invoice.delete()

        return True
