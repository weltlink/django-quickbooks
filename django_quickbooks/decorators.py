from django.db import connection

from django_quickbooks.settings import qbwc_settings


def realm_connection():
    return qbwc_settings.REALM_CONNECTION_DECORATOR


def base_realm_connection(func):
    def connect(realm, *args, **kwargs):
        return func(realm, *args, **kwargs)

    return connect


def base_realm_tenant_connection(func):
    def connect(realm, *args, **kwargs):
        if hasattr(realm, 'schema_name') and hasattr(connection, 'set_schema'):
            try:
                from django_tenants.utils import get_tenant_model
                connection.set_tenant(get_tenant_model().objects.get(schema_name=realm.schema_name))
            except ImportError:
                raise ModuleNotFoundError(
                    'django-tenants package is not installed: pip install django-quickbooks[tenant]'
                )
        return func(realm, *args, **kwargs)

    return connect
