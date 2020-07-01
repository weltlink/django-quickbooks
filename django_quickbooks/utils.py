import random
import string
from importlib import import_module

from django.utils.six import string_types

from django_quickbooks.exceptions import QBItemServiceNotMapped
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
    return ''.join(random.choice(letters) for i in range(length))


def convert_qbd_model_to_qbdtask(obj, qb_resource, qb_operation=None, **kwargs):
    from django_quickbooks import QUICKBOOKS_ENUMS
    from django.contrib.contenttypes.models import ContentType

    if not qb_operation:
        if obj.is_qbd_obj_created:
            qb_operation = QUICKBOOKS_ENUMS.OPP_MOD
        else:
            qb_operation = QUICKBOOKS_ENUMS.OPP_ADD

        return dict(
            qb_operation=qb_operation,
            qb_resource=qb_resource,
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )


def map_item_services_with_charge_types(mapped_items, realm_id):
    """
    :param list of dict mapped_items: Map between external charge types and QBD item services. Example syntax:
        [
            {
                'charge_id': uuid or another type of ID,
                'service_id': QBD item service's ID
            }
        ]
    :param str realm_id: Realm ID of the schema
    :return:
    """
    from django_quickbooks.models import ItemService

    for item in mapped_items:
        item_service = ItemService.objects.get(id=item['service_id'], realm_id=realm_id)
        item_service.external_item_service.create(external_item_service_id=item['charge_id'])


def check_mapping(charge_ids, realm_id):
    """
    Call this function before sending signal to create Invoice or InvoiceLine
    :param list charge_ids: List of charge types IDs
    :param str realm_id: Realm ID of the schema
    :return:
    """
    from django_quickbooks.models import ItemService

    if any([not ItemService.objects.filter(realm_id=realm_id, external_item_service__external_item_service_id=charge_id)
            for charge_id in charge_ids]):
        raise QBItemServiceNotMapped


def filter_objects(realm_id, model, filter_by='ALL'):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :param str filter_by: There are three types of filters: ALL, SYNC, NOT_SYNC
        ALL - returns all objects;
        SYNC - return objects, that were synchronized with Quickbooks;
        NOT_SYNC - returns objects, that were added to django_quickbooks, but not sync with Quickbooks.
    :return: QuerySet of external objects IDs
    """

    def parse_filter():
        filter_params = dict(SYNC=False, NOT_SYNC=True)
        return {
            f'list_id__isnull': filter_params.get(filter_by, False),
            'realm_id': realm_id
        }

    filter_model = import_from_string(f'django_quickbooks.models.{model}', None)

    if filter_by == 'ALL':
        return filter_model.objects.filter(realm_id=realm_id).values_list('external_id', flat=True)

    return filter_model.objects.filter(**parse_filter()).values_list('external_id', flat=True)


def get_time_created(realm_id, model, external_id):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :param str external_id: External object ID of Invoice or Customer
    :return:
    """
    qbd_model = import_from_string(f'django_quickbooks.models.{model}', None)

    obj = qbd_model.objects.filter(external_id=external_id, realm_id=realm_id).first()

    return obj.time_created if obj else None


def get_time_modified(realm_id, model, external_id):
    """
    :param str realm_id: Realm ID of the schema
    :param str model: Model name, e.g. Invoice or Customer
    :param str external_id: External object ID of Invoice or Customer
    :return:
    """
    qbd_model = import_from_string(f'django_quickbooks.models.{model}', None)

    obj = qbd_model.objects.filter(external_id=external_id, realm_id=realm_id).first()

    return obj.time_modified if obj else None
