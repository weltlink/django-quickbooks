import random
import string
from importlib import import_module

from django.utils.six import string_types
from django_quickbooks.settings import DEFAULTS


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
    # FIXME: Should be dependant on realm not on settings.py
    if DEFAULTS['QB_TYPE'] == "QBFS":
        xml_type = 'qbxml version="13.0"'
    elif DEFAULTS['QB_TYPE'] == "QBPOS":
        xml_type = 'qbposxml version="1.0"'
    elif not DEFAULTS['QB_TYPE']:
        raise NotImplementedError(
            f"QB_TYPE not found, Please Check QB_TYPE is present in DEFAULTS dict in settings.py,"
            f" acceptable values= ['QBFS', 'QBPOS']")
    else:
        raise NotImplementedError(
            f"QB_TYPE not correct, Please Check QB_TYPE in DEFAULTS dict in settings.py,"
            f" acceptable values= ['QBFS', 'QBPOS']")

    return f'<?xml version="1.0"?><?{xml_type}?>'


def random_string(length=10):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))
