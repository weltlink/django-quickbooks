from django.contrib import admin
from django.utils.html import format_html

from django_quickbooks import get_queue_manager_class
from django_quickbooks import get_realm_model, get_realm_session_model
from django_quickbooks.forms import CustomerForm, InvoiceLineForm, InvoiceForm, ItemServiceForm, RealmSessionForm, \
    BillAddressForm, ShipAddressForm
from django_quickbooks.models import Invoice, Customer, InvoiceLine, ItemService, BillAddress, ShipAddress, \
    ExternalItemService, ServiceAccount
from django_quickbooks.session_manager import SessionManager

Realm = get_realm_model()
RealmSession = get_realm_session_model()
QueueManager = get_queue_manager_class()


class RealmAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'file_link']

    def file_link(self, obj: Realm):
        if obj.file:
            return format_html(f'<a href="{obj.file.url}">Download QWC</a>')
        return 'No attachments'

    file_link.short_description = 'File'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            obj.set_password(obj.password)
            obj.save()


class RealmSessionAdmin(admin.ModelAdmin):
    form = RealmSessionForm
    list_display = ['__str__', 'id', 'created_at', 'ended_at']
    list_filter = ['realm', 'ended_at']

    def delete_model(self, request, obj):
        SessionManager(queue_manager=QueueManager()).close_session(realm=obj.realm)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ['id', 'name', 'realm']
    list_filter = ['realm']


class InvoiceLineAdmin(admin.ModelAdmin):
    form = InvoiceLineForm


class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    list_display = ['id', 'realm', 'customer']
    list_filter = ['realm']


class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'realm']
    list_filter = ['realm']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False


class ItemServiceAdmin(admin.ModelAdmin):
    form = ItemServiceForm
    list_display = ['id', 'name', 'realm', 'account']
    list_filter = ['realm']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False


class BillAddressAdmin(admin.ModelAdmin):
    form = BillAddressForm
    list_display = ['id', 'customer', 'city', 'state']


class ShipAddressAdmin(admin.ModelAdmin):
    form = ShipAddressForm
    list_display = ['id', 'customer', 'city', 'state']


admin.site.register(Realm, RealmAdmin)
admin.site.register(RealmSession, RealmSessionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(InvoiceLine, InvoiceLineAdmin)
admin.site.register(ItemService, ItemServiceAdmin)
admin.site.register(BillAddress, BillAddressAdmin)
admin.site.register(ShipAddress, ShipAddressAdmin)
admin.site.register(ExternalItemService)
admin.site.register(ServiceAccount, ServiceAccountAdmin)
