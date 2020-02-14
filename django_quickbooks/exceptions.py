from django.utils.translation import ugettext_lazy as _


class ValidationCode:
    REQUIRED = 'required'
    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'
    INVALID_TYPE = 'invalid_type'


VALIDATION_MESSAGES = {
    ValidationCode.REQUIRED: _('This field is required'),
    ValidationCode.MIN_LENGTH: _('The minimum length for the field is %s'),
    ValidationCode.MAX_LENGTH: _('The maximum length for the field is %s'),
    ValidationCode.INVALID_TYPE: _('Invalid type %s for the field type %s'),
}


def _get_error_details(detail, code):
    return {code: detail}


class QbException(Exception):
    detail = 'Quickbooks exception error'

    def __init__(self, error=None):
        if error:
            self.detail = error


class ValidationError(Exception):
    default_detail = _('Invalid attribute.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # Several errors may be collected together, thus
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class ValidationOptionNotFound(QbException):
    pass


class QBXMLParseError(QbException):
    pass


class QBXMLStatusError(QbException):
    pass


class QBOperationNotFound(QbException):
    pass


class QBObjectNotImplemented(QbException):
    pass


class QBObjectServiceNotImplemented(QbException):
    pass
