from django.dispatch import Signal

qbd_task_create = Signal(providing_args=[
    "qb_operation",
    "qb_resource",
    "object_id",
    "content_type",
    "schema_name",
    "instance",
])

customer_created = Signal(providing_args=["qbd_model_mixin_obj", "schema_name"])
customer_updated = Signal(providing_args=["qbd_model_mixin_obj", "schema_name"])
invoice_created = Signal(providing_args=["qbd_model_mixin_obj", "schema_name"])
invoice_updated = Signal(providing_args=["qbd_model_mixin_obj", "schema_name"])
qbd_first_time_connected = Signal(providing_args=["schema_name"])

from django_quickbooks.signals.customer import *
from django_quickbooks.signals.invoice import *
from django_quickbooks.signals.qbd_task import *
