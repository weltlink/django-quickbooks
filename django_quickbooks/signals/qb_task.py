from django.dispatch import receiver

from django_quickbooks import get_qb_task_model, QUICKBOOKS_ENUMS, get_realm_model
from django_quickbooks.signals import qb_task_create

QBTaskModel = get_qb_task_model()
RealmModel = get_realm_model()


@receiver(qb_task_create)
def create_qb_task(sender, qb_operation, qb_resource, object_id, content_type, schema_name, instance=None, *args, **kwargs):
    realm = RealmModel.objects.get(schema_name=schema_name)
    data = dict(
        qb_resource=qb_resource,
        object_id=object_id,
        content_type=content_type,
        realm=realm
    )

    if QBTaskModel.objects \
            .filter(qb_operation=qb_operation, **data) \
            .count():
        return

    if qb_operation == QUICKBOOKS_ENUMS.OPP_MOD and QBTaskModel.objects \
            .filter(qb_operation=QUICKBOOKS_ENUMS.OPP_ADD, **data) \
            .count():
        return

    QBTaskModel.objects.create(qb_operation=qb_operation, **data)
