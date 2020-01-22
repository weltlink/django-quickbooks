from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone


class RealmQuerySet(models.QuerySet):
    def find(self, username, password):
        try:
            realm = self.get(id=username)
            if realm.check_password(password):
                return realm
        except ObjectDoesNotExist:
            pass
        return None


class RealmSessionQuerySet(models.QuerySet):
    def is_active(self, realm):
        try:
            return self.get(realm=realm, ended_at__isnull=True) is not None
        except ObjectDoesNotExist:
            return False

    def close_session(self, realm):
        self.filter(realm=realm, ended_at__isnull=True).update(ended_at=timezone.now())


class QBDTaskQuerySet(models.QuerySet):
    pass
