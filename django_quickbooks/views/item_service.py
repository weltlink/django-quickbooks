import json

from django.http import HttpResponse
from django.views import View

from django_quickbooks.models import ItemService


class ItemServiceView(View):
    def get(self, request, *args, **kwargs):
        item_services = ItemService.objects.values('id', 'name')
        data = list(dict(**{key: str(value) for key, value in item_service.items()}) for item_service in item_services)

        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf8', status=200)
