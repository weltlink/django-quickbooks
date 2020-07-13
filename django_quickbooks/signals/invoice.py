from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Invoice, Customer, InvoiceLine, ItemService
from django_quickbooks.signals import invoice_created, invoice_updated, qbd_task_create, invoice_deleted

RealmModel = get_realm_model()


@receiver(invoice_created)
def create_qbd_invoice(sender, model_obj, realm_id, customer_name, customer_id, invoice_lines=None,
                       is_pending=True, due_date=None, *args, **kwargs):
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
    :param list args: args
    :param dict kwargs: kwargs
    :return:
    """

    customer, _ = Customer.objects.get_or_create(
        name=customer_name,
        realm_id=realm_id,
        defaults=dict(
            external_id=customer_id
        )
    )

    invoice = Invoice.objects.create(
        customer=customer,
        is_pending=is_pending,
        due_date=due_date,
        external_id=model_obj.id,
        realm_id=realm_id,
    )

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
                rate=invoice_line['amount'],
                external_id=invoice_line['charge_id']
            ))
        InvoiceLine.objects.bulk_create(creations)


@receiver(invoice_updated)
def update_qbd_invoice(sender, model_obj, realm_id, is_pending, *args, **kwargs):
    invoice = Invoice.objects.filter(external_id=model_obj.id, realm_id=realm_id).first()

    if invoice:
        invoice.is_pending = is_pending
        invoice.save()


@receiver(invoice_deleted)
def delete_qbd_invoice(sender, model_obj_id, realm_id, *args, **kwargs):
    invoice = Invoice.objects.filter(external_id=model_obj_id, realm_id=realm_id).first()

    if invoice:
        qbd_task_create.send(
            sender=Invoice,
            qb_operation=QUICKBOOKS_ENUMS.OPP_VOID,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
            object_id=invoice.id,
            content_type=ContentType.objects.get_for_model(Invoice),
            realm_id=realm_id,
        )

        invoice.delete()


@receiver(post_save, sender=Invoice)
def create_invoice(sender, instance: Invoice, raw, created, *args, **kwargs):
    if created and not instance.list_id:
        qbd_task_create.send(
            sender=Invoice,
            qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(Invoice),
            realm_id=instance.realm.id
        )
    else:
        qbd_task_create.send(
            sender=Invoice,
            qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(Invoice),
            realm_id=instance.realm.id
        )
