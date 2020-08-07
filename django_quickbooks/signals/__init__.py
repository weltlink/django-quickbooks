from django.dispatch import Signal

qbd_task_create = Signal(providing_args=[
    "qb_operation",
    "qb_resource",
    "object_id",
    "content_type",
    "realm_id",
    "instance",
])

customer_created = Signal(["model_obj_id", "realm_id", "full_name", "company_name", "phone", "email", "bill_address",
                           "ship_address", "updated_at"])
customer_updated = Signal(["model_obj_id", "realm_id", "full_name", "company_name", "phone", "email", "updated_at"])
customer_external_bind = Signal(["customer_id", "external_id", "external_updated_at"])
invoice_created = Signal(["model_obj_id", "realm_id", "customer_name", "customer_id", "invoice_lines", "is_pending",
                          "due_date", "updated_at"])
invoice_updated = Signal(["model_obj_id", "realm_id", "is_pending", "updated_at", "invoice_lines"])
invoice_deleted = Signal(["model_obj_id", "realm_id"])
item_service_deleted = Signal(["model_obj_id", "name", "realm_id", ])
realm_authenticated = Signal(["realm"])
qbd_first_time_connected = Signal(["realm_id"])

from django_quickbooks.signals.customer import *
from django_quickbooks.signals.invoice import *
from django_quickbooks.signals.qbd_task import *
from django_quickbooks.signals.item_service import *
from django_quickbooks.signals.connect import *
