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
            connection.set_schema(realm.schema_name)
        return func(realm, *args, **kwargs)

    return connect
