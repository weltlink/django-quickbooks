import random
import string
from importlib import import_module

from django.utils.six import string_types


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
