from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import ValidationOptionNotFound


def obj_type_validator(value):
    from django_quickbooks.objects.base import BaseObject
    return isinstance(value, BaseObject)


def list_type_validator(value):
    return isinstance(value, list)


def is_primitive(value):
    from django_quickbooks.objects.base import BaseObject
    return isinstance(type(value), type) and not isinstance(value, (BaseObject, list))


def operation_type(value):
    for key, val in value.fields.items():
        if val['validator']['type'] == SchemeValidator.IDTYPE:
            has_attr = hasattr(value, key)
            if 'Txn' in key and has_attr:
                return QUICKBOOKS_ENUMS.OPP_MOD
            if 'Txn' in key and not has_attr:
                return QUICKBOOKS_ENUMS.OPP_ADD
            if not has_attr:
                return QUICKBOOKS_ENUMS.OBJ_REF
            if has_attr:
                return QUICKBOOKS_ENUMS.OPP_ADD
    return ''


def is_list(value):
    return isinstance(value, list)


def str_type_validator(value):
    return isinstance(value, str)


def id_type_validator(value):
    return str_type_validator(value)


def bool_type_validator(value):
    return isinstance(value, int) and value in [1, 0, 'true', 'false']


def min_length_validator(value, length):
    return len(value) >= length


def max_length_validator(value, length):
    return len(value) <= length


def float_type_validator(value):
    return isinstance(value, float)


class SchemeValidator:
    STRTYPE = 'STRTYPE'
    IDTYPE = 'IDTYPE'
    BOOLTYPE = 'BOOLTYPE'
    OBJTYPE = 'OBJTYPE'
    LISTTYPE = 'LISTTYPE'
    FLOATTYPE = 'FLOATTYPE'

    type_validators = dict(
        STRTYPE=str_type_validator,
        IDTYPE=id_type_validator,
        BOOLTYPE=bool_type_validator,
        OBJTYPE=obj_type_validator,
        LISTTYPE=list_type_validator,
        FLOATTYPE=float_type_validator,
    )
    option_validators = dict(
        min_length=min_length_validator,
        max_length=max_length_validator,
    )

    def validate(self, value, **options):
        validator = options.pop('validator')
        required = options.pop('required', False)
        typ = validator['type']

        if not value and not required:
            return True

        if not self.type_validators[typ](value):
            return False

        for value, key in options.items():
            if value not in self.option_validators:
                raise ValidationOptionNotFound
            if not self.option_validators[value](key):
                return False

        return True
