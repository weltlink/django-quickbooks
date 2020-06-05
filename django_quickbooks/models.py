from abc import abstractmethod
from itertools import starmap
from uuid import uuid4, uuid1

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from lxml import etree
from django_quickbooks.objects.customer import Customer as QBDCustomer
from django_quickbooks.objects.address import BillAddress as QBDBillAddress
from django_quickbooks.objects.invoice import Invoice as QBDInvoice

from django_quickbooks import qbwc_settings, QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import QBOperationNotFound
from django_quickbooks.managers import RealmQuerySet, RealmSessionQuerySet, QBDTaskQuerySet
from django_quickbooks.objects import import_object_cls, ItemService as QBDItemService, InvoiceLine as QBDInvoiceLine


class RealmMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=155)
    password = models.CharField(max_length=128, null=True)

    objects = RealmQuerySet.as_manager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    class Meta:
        abstract = True


class RealmSessionMixin(models.Model):
    id = models.UUIDField(verbose_name='Ticket for QBWC session', primary_key=True, editable=False, default=uuid1)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)

    objects = RealmSessionQuerySet.as_manager()

    def close(self):
        self.ended_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class QBDTaskMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    qb_operation = models.CharField(max_length=25)
    qb_resource = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    objects = QBDTaskQuerySet.as_manager()

    def get_request(self):
        obj_class = import_object_cls(self.qb_resource)
        service = obj_class.get_service()()
        obj = self.content_object if self.content_type and self.object_id else None

        if self.qb_operation == QUICKBOOKS_ENUMS.OPP_QR:
            return service.all()
        elif not obj:
            raise ObjectDoesNotExist
        elif self.qb_operation == QUICKBOOKS_ENUMS.OPP_MOD:
            return service.update(obj.to_qbd_obj())
        elif self.qb_operation == QUICKBOOKS_ENUMS.OPP_ADD:
            return service.add(obj.to_qbd_obj())
        elif self.qb_operation == QUICKBOOKS_ENUMS.OPP_DEL:
            return service.delete(obj.to_qbd_obj())
        elif self.qb_operation == QUICKBOOKS_ENUMS.OPP_VOID:
            return service.void(obj.to_qbd_obj())
        else:
            raise QBOperationNotFound


# Below models are concrete implementations of above classes
# As initially I was working with django-tenant-schemas package I had to convert to that architecture
# Thus, below models are extended with schema_name concept that is the core of the django-tenant-schemas package:
# For more information: https://github.com/bernardopires/django-tenant-schemas

# NOTICE: you also find decorators in the package that only work with django-tenant-schemas


class Realm(RealmMixin):
    schema_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = False


class RealmSession(RealmSessionMixin):
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, related_name='sessions')

    class Meta:
        abstract = False


class QBDTask(QBDTaskMixin):
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, related_name='qb_tasks')

    class Meta:
        abstract = False


class QBDModelMixin(models.Model):
    qbd_object_id = models.CharField(max_length=127, unique=True, null=True, editable=False)
    qbd_object_updated_at = models.DateTimeField(null=True, editable=False)
    qbd_object_version = models.CharField(max_length=127, null=True, editable=False)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE, related_name='%(class)ss_realm')

    class Meta:
        abstract = True

    @property
    def is_qbd_obj_created(self):
        return self.qbd_object_id and self.qbd_object_version

    @abstractmethod
    def to_qbd_obj(self, **fields):
        pass

    @classmethod
    def from_qbd_obj(cls, qbd_obj):
        return None


class Customer(QBDModelMixin):
    id = models.CharField(max_length=36, primary_key=True, blank=False, editable=False)
    full_name = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=41, null=True)
    is_active = models.BooleanField(default=True)
    time_created = models.DateTimeField(null=True)
    time_modified = models.DateTimeField(null=True)
    edit_sequence = models.CharField(max_length=127, null=True)
    company_name = models.CharField(max_length=41, null=True)
    phone = models.CharField(max_length=21, null=True)
    alt_phone = models.CharField(max_length=21, null=True)
    fax = models.CharField(max_length=21, null=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=41, null=True)
    alt_contact = models.CharField(max_length=41, null=True)
    external_id = models.CharField(max_length=36, null=True)
    external_updated_at = models.DateTimeField(null=True)

    def to_qbd_obj(self, **fields):
        if fields:
            data = dict(
                starmap(lambda key, value: (key, getattr(self, value)), fields.items())
            )
        else:
            data = dict(
                Name=self.name,
                IsActive=self.is_active,
            )
            if self.is_qbd_obj_created:
                data.update(
                    **dict(
                        ListID=self.qbd_object_id,
                        EditSequence=self.qbd_object_version
                    )
                )
        return QBDCustomer(**data)


class Invoice(QBDModelMixin):
    id = models.CharField(max_length=36, primary_key=True, blank=False, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='invoice')
    time_created = models.DateTimeField(null=True)
    time_modified = models.DateTimeField(null=True)
    edit_sequence = models.CharField(max_length=127, null=True)
    txn_date = models.DateField(null=True)
    is_pending = models.BooleanField(null=True)
    due_date = models.DateField(null=True)
    memo = models.TextField(null=True, max_length=4095)
    external_id = models.CharField(max_length=36, null=True)
    external_updated_at = models.DateTimeField(null=True)

    def to_qbd_obj(self, create=True, **fields):
        def get_bill_address(invoice):
            bill_address = dict(Addr1='', City='', State='', PostalCode='', Country='')

            if hasattr(invoice, 'billaddress'):
                bill_address.update(
                    Addr1=invoice.billaddress.addresses.get('Addr1', ''),
                    City=invoice.billaddress.city or '',
                    State=invoice.billaddress.state or '',
                    PostalCode=str(invoice.billaddress.postal_code) or '',
                    Country=invoice.billaddress.country or '',
                )

            return QBDBillAddress(**bill_address)

        def get_invoice_lines(invoice):
            invoice_lines = []
            for charge in invoice.charges.all():
                item_group = QBDItemService(ListID=charge.type.qbd_object_id if charge.type.qbd_object_id else '')
                invoice_lines.append(QBDInvoiceLine(Item=item_group, Quantity=1.00, Rate=float(charge.amount)))
            return invoice_lines

        data = dict(
            Customer=self.customer.to_qbd_obj(**dict(ListID='qbd_object_id')),
            BillAddress=get_bill_address(self),
            IsPending=self.is_pending,
            DueDate=self.due_date.isoformat(),
            InvoiceLine=get_invoice_lines(self),
        )
        if self.is_qbd_obj_created:
            data.update(
                **dict(
                    TxnID=self.qbd_object_id,
                    EditSequence=self.qbd_object_version
                )
            )

        return QBDInvoice(**data)


class ItemService(QBDModelMixin):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)
    name = models.CharField(max_length=25, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)

    def to_qbd_obj(self, **fields):
        data = dict(
            Name=self.name
        )
        if self.is_qbd_obj_created:
            data.update(
                **dict(
                    ListID=self.qbd_object_id,
                    EditSequence=self.qbd_object_version
                )
            )

        return QBDItemService(**data)

    @classmethod
    def from_qbd_obj(cls, qbd_obj):
        return cls(
            name=qbd_obj.Name,
            qbd_object_id=qbd_obj.ListID,
            qbd_object_updated_at=timezone.now() + timezone.timedelta(minutes=1),
            qbd_object_version=qbd_obj.EditSequence
        )


class InvoiceLine(QBDModelMixin):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='charges')
    type = models.ForeignKey(ItemService, on_delete=models.SET_NULL, null=True, related_name='invoice_charges')
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    note = models.TextField(max_length=150, null=True, blank=True)
    external_id = models.CharField(max_length=36, null=True)

    def to_qbd_obj(self, **fields):
        pass


class ExternalItemService(models.Model):
    charge_type = models.ForeignKey(ItemService, on_delete=models.CASCADE, related_name='external_item_service')
    external_item_service_id = models.CharField(max_length=36, null=False, blank=False)


class AbstractAddress(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='%(class)s')
    addresses = JSONField(default=dict)
    city = models.CharField(max_length=31, null=True)
    state = models.CharField(max_length=21, null=True)
    postal_code = models.CharField(max_length=13, null=True)
    country = models.CharField(max_length=31, null=True)
    note = models.CharField(max_length=41, null=True)

    class Meta:
        abstract = True


class BillAddress(AbstractAddress):
    pass


class ShipAddress(AbstractAddress):
    pass


def create_qwc(realm, **kwargs):
    root = etree.Element("QBWCXML")

    app_name = kwargs.pop('app_name', qbwc_settings.APP_NAME)
    msg = etree.SubElement(root, 'AppName')
    msg.text = str(app_name)

    app_id = kwargs.pop('app_id', qbwc_settings.APP_ID)
    msg = etree.SubElement(root, 'AppID')
    msg.text = str(app_id)

    app_url = kwargs.pop('app_url', qbwc_settings.APP_URL)
    msg = etree.SubElement(root, 'AppURL')
    msg.text = str(app_url)

    app_desc = kwargs.pop('app_desc', qbwc_settings.APP_DESCRIPTION)
    msg = etree.SubElement(root, 'AppDescription')
    msg.text = str(app_desc)

    app_support = kwargs.pop('app_support', qbwc_settings.APP_SUPPORT)
    msg = etree.SubElement(root, 'AppSupport')
    msg.text = str(app_support)

    username = realm.id
    msg = etree.SubElement(root, 'UserName')
    msg.text = str(username)

    owner_id = kwargs.pop('owner_id', qbwc_settings.OWNER_ID)
    msg = etree.SubElement(root, 'OwnerID')
    msg.text = str(owner_id)

    file_id = kwargs.pop('file_id', '{%s}' % uuid1())
    msg = etree.SubElement(root, 'FileID')
    msg.text = str(file_id)

    qb_type = kwargs.pop('qb_type', qbwc_settings.QB_TYPE)
    msg = etree.SubElement(root, 'QBType')
    msg.text = str(qb_type)

    msg = etree.SubElement(root, 'Scheduler')

    schedule_n_minutes = kwargs.pop('schedule_n_minutes', qbwc_settings.MINIMUM_RUN_EVERY_NMINUTES)
    n_minutes = etree.SubElement(msg, 'RunEveryNMinutes')
    n_minutes.text = str(schedule_n_minutes)

    tree = etree.ElementTree(root)

    return etree.tostring(tree, xml_declaration=True, encoding='UTF-8')
