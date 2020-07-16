import random
import string
from importlib import import_module
from itertools import groupby

from django.utils.six import string_types

from django_quickbooks.settings import import_from_string


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def xml_encode(value: str):
    transform = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
    }
    for transform_key, transform_value in transform.items():
        value = value.replace(transform_key, transform_value)
    return value


def xml_setter(name, value, encode=False, **options):
    option_xml = ''

    for option_key, option_value in options.items():
        option_value = xml_encode(option_value) if encode else option_value
        option_xml += '%s="%s" ' % (option_key, option_value)
    option_xml = option_xml.strip()

    value = xml_encode(value) if encode else value
    return '<%s>%s</%s>' % (name, value, name) if not option_xml else '<%s %s>%s</%s>' % (name, option_xml, value, name)


def get_xml_meta_info():
    return '<?xml version="1.0"?><?qbxml version="13.0"?>'


def random_string(length=10):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


def map_item_services_with_external_item_services(mapped_items, realm_id):
    """
    :param list of dict mapped_items: Map between external item services and QBD item services. Example syntax:
        [
            {
                'external_ids': list of uuid or another type of ID,
                'service_id': QBD item service's ID
            }
        ]
    :param str realm_id: Realm ID of the schema
    :return:
    """
    from django_quickbooks.models import ItemService, ExternalItemService

    for obj in mapped_items:
        item_service = ItemService.objects.get(id=obj['service_id'], realm_id=realm_id)
        ExternalItemService.object.set(
            realm_id=realm_id,
            item_service=item_service,
            external_item_service_ids=obj['external_ids']
        )


def check_mapping(external_ids, realm_id):
    """
    Call this function before sending signal to create Invoice or InvoiceLine
    :param list of str external_ids: List of charge types IDs
    :param str realm_id: Realm ID of the schema
    :return: bool
    """
    from django_quickbooks.models import ExternalItemService

    if any([not ExternalItemService.objects.filter(item_service__realm_id=realm_id,
                                                   external_item_service_id=external_id)
            for external_id in external_ids]):
        return False

    return True


def get_mapped_services(external_ids, realm_id):
    """
    :param list of str external_ids: List of charge types IDs
    :param str realm_id: Realm ID of the schema
    :return: list of dict
    """
    from django_quickbooks.models import ExternalItemService
    from django_quickbooks.models import ItemService

    def key(x):
        return x.item_service.id

    item_services = ExternalItemService.objects.filter(
        item_service__realm_id=realm_id,
        external_item_service_id__in=external_ids)

    mapped_services = []
    for item_service, group in groupby(sorted(item_services, key=key), key=key):
        item_service = ItemService.objects.get(id=item_service)
        mapped_services.append(dict(
            external_ids=list(gr.external_item_service_id for gr in list(group)),
            service_id=item_service.id.__str__(),
            name=item_service.name,
            full_name=item_service.full_name,
            parent_id=item_service.parent_id,
        ))

    return mapped_services


def synced_objects(realm_id, model):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :return: List of str of external objects IDs
    """

    qbd_model = import_from_string(f'django_quickbooks.models.{model}', None)
    qbd_objects = qbd_model.objects.filter(list_id__isnull=False, realm_id=realm_id)

    return [str(qbd_object.external_id) for qbd_object in qbd_objects]


def get_time_created(realm_id, model, external_id):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :param str external_id: External object ID of Invoice or Customer
    :return: Datetime or None
    """
    qbd_model = import_from_string(f'django_quickbooks.models.{model}', None)

    obj = qbd_model.objects.filter(external_id=external_id, realm_id=realm_id).first()

    return obj.time_created if obj else None


def get_time_modified(realm_id, model, external_id):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :param str external_id: External object ID of Invoice or Customer
    :return: Datetime or None
    """
    qbd_model = import_from_string(f'django_quickbooks.models.{model}', None)

    obj = qbd_model.objects.filter(external_id=external_id, realm_id=realm_id).first()

    return obj.time_modified if obj else None
