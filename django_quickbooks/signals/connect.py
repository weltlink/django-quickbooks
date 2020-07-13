from django.db.models.signals import post_save
from django.dispatch import receiver

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import ItemService, ServiceAccount, Realm
from django_quickbooks.signals import qbd_task_create


@receiver(post_save, sender=Realm)
def sync_accounts_and_item_services(sender, instance: Realm, raw, created, *args, **kwargs):
    if created:
        qbd_task_create.send(
            sender=ServiceAccount,
            qb_operation=QUICKBOOKS_ENUMS.OPP_QR,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT,
            object_id=None,
            content_type=None,
            realm_id=instance.id,
        )

        qbd_task_create.send(
            sender=ItemService,
            qb_operation=QUICKBOOKS_ENUMS.OPP_QR,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE,
            object_id=None,
            content_type=None,
            realm_id=instance.id,
        )
