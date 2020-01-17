from django.apps import AppConfig


class DjangoQuickbooksConfig(AppConfig):
    name = 'django_quickbooks'

    def ready(self):
        import django_quickbooks.signals
