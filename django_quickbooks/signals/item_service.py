from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import ItemService
from django_quickbooks.signals import qbd_task_create, item_service_deleted


@receiver(post_save, sender=ItemService)
def create_qbd_item_service(sender, instance: ItemService, raw, created, *args, **kwargs):
    if created:
        qbd_task_create.send(
            sender=ItemService,
            qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(ItemService),
            realm_id=instance.realm.id
        )


@receiver(item_service_deleted)
def delete_qbd_item_service(sender, model_obj_id, realm_id, *args, **kwargs):
    item_service = ItemService.objects.get(realm_id=realm_id,
                                           external_item_service__external_item_service_id=model_obj_id)
    item_service.external_item_service.get(external_item_service_id=model_obj_id).delete()
