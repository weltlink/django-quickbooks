from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.models import ItemService
from django_quickbooks.signals import item_service_created, qbd_task_create, item_service_deleted


@receiver(item_service_created)
def create_qbd_item_service(sender, model_obj_id, name, realm_id):
    item_service, created = ItemService.objects.get_or_create(name=name, realm_id=realm_id)
    item_service.external_item_service.get_or_create(external_item_service_id=model_obj_id)

    if created:
        qbd_task_create.send(
            sender=ItemService,
            qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
            qb_resource=QUICKBOOKS_ENUMS.RESOURCE_ITEM_SERVICE,
            object_id=item_service.id,
            content_type=ContentType.objects.get_for_model(ItemService),
            realm_id=realm_id
        )


@receiver(item_service_deleted)
def delete_qbd_item_service(sender, model_obj_id, name, realm_id):
    item_service: ItemService = ItemService.objects.get(name=name, realm_id=realm_id)
    item_service.external_item_service.get(external_item_service_id=model_obj_id).delete()
