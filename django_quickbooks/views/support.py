from django.http import HttpResponse
from django.views import View


class Support(View):

    def get(self, request, *args, **kwargs):
        html = "<html><body>Example of a supports page</body></html>"

        return HttpResponse(html)
