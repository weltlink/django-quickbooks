from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from accounting import ChargeType
from django_quickbooks import get_realm_model
from django_quickbooks.objects.invoice import Item
from django_quickbooks.services.invoice import ItemService
from django_quickbooks.signals import qbd_first_time_connected
from django_quickbooks.tasks import build_request

RealmModel = get_realm_model()


@receiver(qbd_first_time_connected)
def set_first_time_configurations(sender, schema_name, *args, **kwargs):
    try:
        realm = RealmModel.objects.get(schema_name=schema_name)
        if realm.is_active:
            for charge in ChargeType.CHARGE_TYPES:
                request_body = ItemService().add(Item(Name=charge[0]))
                build_request.delay(request_body, realm.id)
    except ObjectDoesNotExist:
        pass
