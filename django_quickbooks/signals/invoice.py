from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Invoice, Customer
from django_quickbooks.signals import invoice_created, invoice_updated, qbd_task_create, customer_created

RealmModel = get_realm_model()


@receiver(invoice_created)
def create_qbd_invoice(sender, qbd_model_mixin_obj, realm_id, customer_name, customer_id,
                       is_pending=True, due_date=None, bill_address=None, ship_address=None, *args, **kwargs):
    try:
        customer = Customer.objects.get(name=customer_name, realm_id=realm_id)
    except ObjectDoesNotExist:
        customer = Customer.objects.create(name=customer_name, external_id=customer_id, realm_id=realm_id)
        customer_created.send(Customer, qbd_model_mixin_obj=customer, realm_id=realm_id, name=customer_name)

    invoice = Invoice.objects.create(
        customer=customer,
        is_pending=is_pending,
        due_date=due_date,
        external_id=qbd_model_mixin_obj.id,
        realm_id=realm_id,
    )

    if isinstance(bill_address, dict):
        invoice.billaddress.objects.create(**bill_address)

    if isinstance(ship_address, dict):
        invoice.shipaddress.objects.create(**ship_address)

    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        realm_id=realm_id,
    )


@receiver(invoice_updated)
def update_qbd_invoice(sender, qbd_model_mixin_obj, realm_id, is_pending, *args, **kwargs):
    Invoice.objects.filter(external_id=qbd_model_mixin_obj.id, realm_id=realm_id).update(is_pending=is_pending)

    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        realm_id=realm_id,
    )
