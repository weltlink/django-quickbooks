from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.models import Customer, BillAddress, ShipAddress
from django_quickbooks.signals import customer_created, customer_updated, qbd_task_create, customer_external_bind

RealmModel = get_realm_model()


@receiver(customer_created)
def create_qbd_customer(sender, model_obj_id, realm_id, full_name, company_name=None, phone=None, email=None,
                        bill_address=None, ship_address=None, updated_at=None, *args, **kwargs):
    customer, created = Customer.objects.get_or_create(
        full_name=full_name,
        realm_id=realm_id,
        defaults=dict(
            name=full_name.split(':')[-1],
            company_name=company_name,
            phone=phone,
            email=email,
            external_id=model_obj_id,
            external_updated_at=updated_at or timezone.now()
        )
    )

    if created:
        if isinstance(bill_address, dict):
            BillAddress.objects.create(**bill_address, customer=customer)

        if isinstance(ship_address, dict):
            ShipAddress.objects.create(**ship_address, customer=customer)
    else:
        customer.external_id = model_obj_id
        customer.external_updated_at = updated_at or timezone.now()
        customer.save(update_fields=['external_id', 'external_updated_at'])


@receiver(customer_updated)
def update_qbd_customer(sender, model_obj_id, realm_id, full_name, company_name=None, phone=None, email=None,
                        updated_at=None, *args, **kwargs):
    customer = Customer.objects.filter(external_id=model_obj_id, realm_id=realm_id).first()

    if customer:
        customer.full_name = full_name
        customer.name = full_name.split(':')[-1]
        customer.company_name = company_name
        customer.phone = phone
        customer.email = email
        customer.external_updated_at = updated_at or timezone.now()
        customer.save()


# Use this signal when bind external Customer with QBD Customer, this one won't call qbd_task_create signal
@receiver(customer_external_bind)
def bind_qbd_customer_with_external(sender, customer_id, external_id, external_updated_at=None,
                                    *args, **kwargs):
    customer = Customer.objects.get(id=customer_id)
    customer.external_id = external_id
    customer.external_updated_at = external_updated_at or timezone.now()
    customer.save(update_fields=['external_id', 'external_updated_at'])


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
    elif not created and not kwargs.get('update_fields', None):
        qbd_task_create.send(
            sender=Customer,
            qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(Customer),
            realm_id=instance.realm.id,
        )

        instance.full_name = f'{instance.parent.name}:{instance.name}' if instance.parent else instance.name
        instance.save(update_fields=['full_name'])

        for child in Customer.objects.filter(parent=instance):
            child.full_name = f'{instance.name}:{child.name}'
            child.save(update_fields=['full_name'])
