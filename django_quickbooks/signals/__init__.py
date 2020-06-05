from django.dispatch import Signal

qbd_task_create = Signal(providing_args=[
    "qb_operation",
    "qb_resource",
    "object_id",
    "content_type",
    "realm_id",
    "instance",
])

customer_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id", "name", "company_name", "phone", "email"])
customer_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id", "name", "company_name", "phone", "email"])
invoice_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id", "customer_name", "customer_id",
                                         "is_pending", "due_date", "bill_address", "ship_address"])
invoice_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id", "is_pending"])
invoice_line_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id", ])
item_service_created = Signal(providing_args=["model_obj_id", "name", "realm_id", ])
item_service_deleted = Signal(providing_args=["model_obj_id", "name", "realm_id", ])
realm_authenticated = Signal(providing_args=["realm"])
qbd_first_time_connected = Signal(providing_args=["realm_id"])

from django_quickbooks.signals.customer import *
from django_quickbooks.signals.invoice import *
from django_quickbooks.signals.qbd_task import *
