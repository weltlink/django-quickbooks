from django.urls import path
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView

from django_quickbooks.views import QuickBooksService, Support
from django_quickbooks.views.account import AccountView
from django_quickbooks.views.customer import CustomerView
from django_quickbooks.views.item_service import ItemServiceView

urlpatterns = [
    path('quickbooks-desktop/support/', Support.as_view()),
    path('quickbooks-desktop/', DjangoView.as_view(
        services=[QuickBooksService],
        tns='http://developer.intuit.com/',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11())
         ),
    path('quickbooks-desktop/accounts/', AccountView.as_view()),
    path('quickbooks-desktop/item-services/', ItemServiceView.as_view()),
    path('quickbooks-deskuop/customers/', CustomerView.as_view()),
]
