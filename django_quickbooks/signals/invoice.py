from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Invoice, Customer, BillAddress, ShipAddress, InvoiceLine, ItemService
from django_quickbooks.signals import invoice_created, invoice_updated, qbd_task_create, customer_created

RealmModel = get_realm_model()


@receiver(invoice_created)
def create_qbd_invoice(sender, model_obj, realm_id, customer_name, customer_id, invoice_lines=None,
                       is_pending=True, due_date=None, bill_address=None, ship_address=None, *args, **kwargs):
    """
    :param object sender: Sender model
    :param Invoice model_obj: Invoice object
    :param str realm_id: Realm ID of the schema
    :param str customer_name: Customer's name to whom Invoice belonged
    :param srt customer_id: Customer's ID
    :param list of dict invoice_lines: To match this syntax of dict, need to divide charge model into two models.
        First is for charges itself, another is to keep their types through the ForeignKey field.
        [
            {
                'charge_id': uuid or another type of ID,
                'amount': 1278.42,
                'type_id': uuid or another type of ID,
                'name': 'FUEL',
            }
        ]
    :param bool is_pending: Is Invoice pending to be payed or not
    :param date due_date: Invoice DUE date
    :param dict bill_address: Billing address
    :param dict ship_address: Shipping address
    :param list args: args
    :param dict kwargs: kwargs
    :return:
    """

    try:
        customer = Customer.objects.get(name=customer_name, realm_id=realm_id)
    except ObjectDoesNotExist:
        customer = Customer.objects.create(name=customer_name, external_id=customer_id, realm_id=realm_id)
        customer_created.send(Customer, qbd_model_mixin_obj=customer, realm_id=realm_id, name=customer_name)

    invoice = Invoice.objects.create(
        customer=customer,
        is_pending=is_pending,
        due_date=due_date,
        external_id=model_obj.id,
        realm_id=realm_id,
    )

    if isinstance(bill_address, dict):
        BillAddress.objects.create(**bill_address, invoice=invoice)

    if isinstance(ship_address, dict):
        ShipAddress.objects.create(**ship_address, invoice=invoice)

    if isinstance(invoice_lines, list):
        creations = []
        for invoice_line in invoice_lines:
            item_service = ItemService.objects.get(
                realm_id=realm_id,
                external_item_service__external_item_service_id=invoice_line['type_id'])
            creations.append(InvoiceLine(
                invoice=invoice,
                realm_id=realm_id,
                type=item_service,
                amount=invoice_line['amount'],
                external_id=invoice_line['charge_id']
            ))
        InvoiceLine.objects.bulk_create(creations)


@receiver(invoice_updated)
def update_qbd_invoice(sender, model_obj, realm_id, is_pending, *args, **kwargs):
    invoice = Invoice.objects.filter(external_id=model_obj.id, realm_id=realm_id).first()

    if invoice:
        invoice.is_pending = is_pending

        qbd_task_create.send(
            sender=model_obj.__class__,
            qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
            object_id=invoice.id,
            content_type=ContentType.objects.get_for_model(Invoice),
            realm_id=realm_id,
        )
