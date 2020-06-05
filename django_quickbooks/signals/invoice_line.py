from django.db import transaction
from django.dispatch import receiver

from django_quickbooks.models import InvoiceLine, ItemService, Invoice
from django_quickbooks.signals import invoice_line_created, item_service_created


@receiver(invoice_line_created)
def create_qbd_invoice_item(sender, external_invoice_id, invoice_charges, realm_id):
    """

    :param object sender: Sender model
    :param str external_invoice_id: Invoice ID to which charges belonged
    :param list of dict invoice_charges: To match this syntax of dict, need to divide charge model into two models.
        First is for charges itself, another is to keep their types through the ForeignKey field.
        [
            {
                'charge_id': uuid or another type of ID,
                'amount': 1278.42,
                'type_id': uuid or another type of ID,
                'name': 'FUEL',
            }
        ]
    :param str realm_id:
    :return:
    """

    invoice = Invoice.objects.get(external_id=external_invoice_id, realm_id=realm_id)

    with transaction.atomic():
        for invoice_charge in invoice_charges:
            item_service_created.send(
                sender=ItemService,
                model_obj_id=invoice_charge['type_id'],
                name=invoice_charge['name'],
                realm_id=realm_id
            )
            item_service = ItemService.objects.get(name=invoice_charge['name'], realm_id=realm_id)

            InvoiceLine.objects.get_or_create(
                external_id=invoice_charge['charge_id'],
                realm_id=realm_id,
                defaults=dict(
                    amount=invoice_charge['amount'],
                    invoice=invoice,
                    type=item_service,
                    realm_id=realm_id,
                )
            )

