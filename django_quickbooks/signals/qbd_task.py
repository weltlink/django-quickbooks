from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from django_quickbooks import get_qbd_task_model, QUICKBOOKS_ENUMS, get_realm_model
from django_quickbooks.signals import qbd_task_create

QBDTaskModel = get_qbd_task_model()
RealmModel = get_realm_model()


@receiver(qbd_task_create)
def create_qbd_task(sender, qb_operation, qb_resource, object_id, content_type, realm_id, instance=None, *args, **kwargs):
    try:
        realm = RealmModel.objects.get(id=realm_id)
        data = dict(
            qb_resource=qb_resource,
            object_id=object_id,
            content_type=content_type,
            realm=realm
        )

        if QBDTaskModel.objects \
                .filter(qb_operation=qb_operation, **data) \
                .count():
            return

        if qb_operation == QUICKBOOKS_ENUMS.OPP_MOD and QBDTaskModel.objects \
                .filter(qb_operation=QUICKBOOKS_ENUMS.OPP_ADD, **data) \
                .count():
            return

        QBDTaskModel.objects.create(qb_operation=qb_operation, **data)

    except ObjectDoesNotExist:
        pass
