from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Customer, BillAddress, ShipAddress
from django_quickbooks.signals import customer_created, customer_updated, qbd_task_create

RealmModel = get_realm_model()


@receiver(customer_created)
def create_qbd_customer(sender, model_obj_id, realm_id, name, company_name=None, phone=None, email=None,
                        bill_address=None, ship_address=None, *args, **kwargs):
    customer, created = Customer.objects.get_or_create(
        name=name,
        realm_id=realm_id,
        defaults=dict(
            company_name=company_name,
            phone=phone,
            email=email,
            external_id=model_obj_id
        )
    )

    if created:
        if isinstance(bill_address, dict):
            BillAddress.objects.create(**bill_address, customer=customer)

        if isinstance(ship_address, dict):
            ShipAddress.objects.create(**ship_address, customer=customer)


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


@receiver(post_save, sender=Customer)
def create_customer_update_qbd_task(sender, instance: Customer, raw, created, *args, **kwargs):
    if created and not instance.list_id:
        qbd_task_create.send(
            sender=Customer,
            qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(Customer),
            realm_id=instance.realm.id,
        )
    else:
        qbd_task_create.send(
            sender=Customer,
            qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(Customer),
            realm_id=instance.realm.id,
        )
