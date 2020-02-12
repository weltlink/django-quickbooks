from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import VALIDATION_MESSAGES, ValidationCode
from django_quickbooks.exceptions import ValidationOptionNotFound, ValidationError


def obj_type_validator(value):
    from django_quickbooks.objects.base import BaseObject
    return isinstance(value, BaseObject)


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
    if not isinstance(value, list):
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), str),
                              ValidationCode.INVALID_TYPE)


def str_type_validator(value):
    if not isinstance(value, str):
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), str),
                              ValidationCode.INVALID_TYPE)


def es_type_validator(value):
    if not isinstance(value, str) or not value.isnumeric():
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), str),
                              ValidationCode.INVALID_TYPE)


def id_type_validator(value):
    if not isinstance(value, str):
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), str),
                              ValidationCode.INVALID_TYPE)


def bool_type_validator(value):
    if value not in [1, 0, 'true', 'false', '1', '0']:
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), bool),
                              ValidationCode.INVALID_TYPE)


def min_length_validator(value, length):
    if len(value) < length:
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.MIN_LENGTH] % length, ValidationCode.MIN_LENGTH)


def max_length_validator(value, length):
    if len(value) > length:
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.MAX_LENGTH] % length, ValidationCode.MAX_LENGTH)


def float_type_validator(value):
    if not isinstance(value, float):
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), float),
                              ValidationCode.INVALID_TYPE)


def required_validator(value, required=False):
    if not value and required:
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.REQUIRED], ValidationCode.REQUIRED)


def many_validator(value, many=False):
    if not isinstance(value, list) and many:
        raise ValidationError(VALIDATION_MESSAGES[ValidationCode.INVALID_TYPE] % (type(value), list),
                              ValidationCode.INVALID_TYPE)


class SchemeValidator:
    STRTYPE = 'STRTYPE'
    ESTYPE = 'ESTYPE'
    IDTYPE = 'IDTYPE'
    BOOLTYPE = 'BOOLTYPE'
    OBJTYPE = 'OBJTYPE'
    FLOATTYPE = 'FLOATTYPE'

    type_validators = dict(
        STRTYPE=str_type_validator,
        ESTYPE=es_type_validator,
        IDTYPE=id_type_validator,
        BOOLTYPE=bool_type_validator,
        OBJTYPE=obj_type_validator,
        FLOATTYPE=float_type_validator,
    )
    option_validators = dict(
        min_length=min_length_validator,
        max_length=max_length_validator,
    )

    def validate(self, field_name, value, **options):
        errors = []

        required = options.pop('required', False)

        try:
            required_validator(value, required)
        except ValidationError as exc:
            errors.append(exc.detail)

        many = options.pop('many', False)

        try:
            # should be given list type but given something else
            many_validator(value, many)
        except ValidationError as exc:
            errors.append(exc.detail)

        if many:
            for single_value in value:
                try:
                    self.validate(single_value, **options)
                except ValidationError as exc:
                    errors.append(exc.detail)

            if errors:
                raise ValidationError(errors, field_name)

        validator = options.pop('validator')
        typ = validator['type']

        try:
            self.type_validators[typ](value)
        except ValidationError as exc:
            errors.append(exc.detail)

        for value, key in options.items():
            if value not in self.option_validators:
                raise ValidationOptionNotFound
            try:
                self.option_validators[value](key)
            except ValidationError as exc:
                errors.append(exc.detail)

        if errors:
            raise ValidationError(errors, field_name)
