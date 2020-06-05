from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Customer
from django_quickbooks.signals import customer_created, customer_updated, qbd_task_create

RealmModel = get_realm_model()


@receiver(customer_created)
def create_qbd_customer(sender, qbd_model_mixin_obj, realm_id, name, company_name=None, phone=None, email=None,
                        *args, **kwargs):
    Customer.objects.create(
        name=name,
        company_name=company_name,
        phone=phone,
        email=email,
        realm_id=realm_id,
        external_id=qbd_model_mixin_obj.id
    )

    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        realm_id=realm_id,
    )


@receiver(customer_updated)
def update_qbd_customer(sender, qbd_model_mixin_obj, realm_id, name, company_name=None, phone=None, email=None,
                        *args, **kwargs):
    Customer.objects.filter(name=name, realm_id=realm_id).update(
        company_name=company_name,
        phone=phone,
        email=email
    )

    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        realm_id=realm_id,
    )
