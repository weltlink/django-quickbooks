import json

from django.http import HttpResponse
from django.views import View

from django_quickbooks.models import ServiceAccount


class AccountView(View):
    def get(self, request, *args, **kwargs):
        accounts = ServiceAccount.objects.values('id', 'name', 'account_type')
        data = list(dict(**{key: str(value) for key, value in account.items()}) for account in accounts)

        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf8')
