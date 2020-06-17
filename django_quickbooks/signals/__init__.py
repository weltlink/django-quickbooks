from django.dispatch import Signal

qbd_task_create = Signal(providing_args=[
    "qb_operation",
    "qb_resource",
    "object_id",
    "content_type",
    "realm_id",
    "instance",
])

customer_created = Signal(["model_obj_id", "realm_id", "name", "company_name", "phone", "email"])
customer_updated = Signal(["model_obj_id", "realm_id", "name", "company_name", "phone", "email"])
invoice_created = Signal(["model_obj", "realm_id", "customer_name", "customer_id", "invoice_lines"
                          "is_pending", "due_date", "bill_address", "ship_address"])
invoice_updated = Signal(["model_obj", "realm_id", "is_pending"])
invoice_line_created = Signal(["model_obj_id", "realm_id", ])
item_service_deleted = Signal(["model_obj_id", "name", "realm_id", ])
realm_authenticated = Signal(["realm"])
qbd_first_time_connected = Signal(["realm_id"])

from django_quickbooks.signals.customer import *
from django_quickbooks.signals.invoice import *
from django_quickbooks.signals.qbd_task import *
from django_quickbooks.signals.item_service import *
