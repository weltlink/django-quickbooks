from abc import abstractmethod
from uuid import uuid4, uuid1

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from lxml import etree

from django_quickbooks import qbwc_settings, QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import QBOperationNotFound
from django_quickbooks.managers import RealmQuerySet, RealmSessionQuerySet, QBDTaskQuerySet
from django_quickbooks.objects import import_object_cls


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
