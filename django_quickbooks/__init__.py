from django.core.exceptions import ImproperlyConfigured

from django_quickbooks.settings import qbwc_settings
from django_quickbooks.utils import import_callable

HIGHEST_SUPPORTING_QBWC_VERSION = '2.2.0.34'
default_app_config = 'django_quickbooks.apps.DjangoQuickbooksConfig'


def get_session_manager():
    return qbwc_settings.SESSION_MANAGER_CLASS()


class QBWC_CODES:
    NONE = 'none'  # no work to do for the service
    BUSY = 'busy'  # service is busy with other task
    NVU = 'nvu'  # invalid user is sent to the service
    CC = ''  # indicates current company to use for the web connector to proceed further
    CONN_CLS_OK = 'ok'  # indicates web connector and web service _set_connection closed successfully
    CONN_CLS_ERR = 'done'  # indicates web connector failed connecting to web service and finished its job
    INTR_DONE = 'done'  # indicates web connector finished interactive session with web service
    UNEXP_ERR = 'unexpected error'  # unexpected error received from web connector
    CV = ''  # no update needed for web connector to update its version, it can proceed further


class QUICKBOOKS_ENUMS:
    VERSION_13 = 13
    OPP_ADD = 'Add'
    OPP_MOD = 'Mod'
    OPP_QR = 'Query'
    OPP_DEL = 'Del'
    OPP_VOID = 'Void'

    OPERATIONS = (
        (OPP_ADD, 'Add'),
        (OPP_MOD, 'Modify'),
        (OPP_QR, 'Query'),
        (OPP_DEL, 'Delete'),
    )

    OBJ_REF = 'Ref'

    RESOURCE_CUSTOMER = 'Customer'
    RESOURCE_VENDOR = 'Vendor'
    RESOURCE_INVOICE = 'Invoice'
    RESOURCE_BILL = 'Bill'
    RESOURCE_ITEM_SERVICE = 'ItemService'
    RESOURCE_TXN = 'Txn'


class QBXML_RESPONSE_STATUS_CODES:
    OK = '0'
    NO_MATCH = '1'
    ONE_OR_MORE_NOT_FOUND = '500'
    OBJECT_CAN_NOT_BE_RETURNED = '510'
    INTERNAL_ERROR = '1000'
    INVALID_OBJECT_ID = '3000'
    INVALID_BOOLEAN = '3010'
    INVALID_DATE = '3020'
    INVALID_DATE_RANGE = '3030'
    NAME_IS_NOT_UNIQUE = '3100'


def get_processors():
    processors = []
    for processor_class in qbwc_settings.RESPONSE_PROCESSORS:
        processors.append(processor_class)
    if not processors:
        raise ImproperlyConfigured(
            'No processors have been defined. Does '
            'RESPONSE_PROCESSORS for Quickbooks contain anything?'
        )
    return processors


def get_realm_model():
    return qbwc_settings.REALM_MODEL_CLASS


def get_realm_session_model():
    return qbwc_settings.REALM_SESSION_MODEL_CLASS


def get_qbd_task_model():
    return qbwc_settings.QBD_TASK_MODEL_CLASS
