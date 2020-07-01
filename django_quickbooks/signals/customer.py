from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Customer
from django_quickbooks.signals import customer_created, customer_updated, qbd_task_create

RealmModel = get_realm_model()


@receiver(customer_created)
def create_qbd_customer(sender, model_obj_id, realm_id, name, company_name=None, phone=None, email=None,
                        *args, **kwargs):
    customer, _ = Customer.objects.get_or_create(
        name=name,
        realm_id=realm_id,
        defaults=dict(
            company_name=company_name,
            phone=phone,
            email=email,
            external_id=model_obj_id
        )
    )

    qbd_task_create.send(
        sender=Customer,
        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
        object_id=customer.id,
        content_type=ContentType.objects.get_for_model(Customer),
        realm_id=realm_id,
    )


@receiver(customer_updated)
def update_qbd_customer(sender, model_obj_id, realm_id, name, company_name=None, phone=None, email=None,
                        *args, **kwargs):
    customer = Customer.objects.filter(name=name, realm_id=realm_id, external_id=model_obj_id).first()

    if customer:
        customer.name = name,
        customer.company_name = company_name
        customer.phone = phone
        customer.email = email
        customer.save()

        qbd_task_create.send(
            sender=Customer,
            qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
            object_id=customer.id,
            content_type=ContentType.objects.get_for_model(Customer),
            realm_id=realm_id,
        )
