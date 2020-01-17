from django.urls import path
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView

from django_quickbooks.views import QuickBooksService, Support

urlpatterns = [
    path('quickbooks-desktop/support/', Support.as_view()),
    path('quickbooks-desktop/', DjangoView.as_view(
        services=[QuickBooksService],
        tns='http://developer.intuit.com/',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11())
         ),
]

