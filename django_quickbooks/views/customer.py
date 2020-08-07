import json

from django.http import HttpResponse
from django.views import View

from django_quickbooks.models import Customer


class CustomerView(View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        data = list(dict(
            id=customer.id.__str__(),
            name=customer.name,
            is_active=customer.is_active,
            phone=customer.phone,
            alt_phone=customer.alt_phone,
            fax=customer.fax,
            email=customer.email,
            contact=customer.contact,
            alt_contact=customer.alt_contact,
            external_id=customer.external_id,
        ) for customer in customers)

        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf8')
