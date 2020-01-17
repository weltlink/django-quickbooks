from django.contrib import admin

from django_quickbooks import get_realm_model, get_realm_session_model

Realm = get_realm_model()
RealmSession = get_realm_session_model()


class RealmAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            obj.set_password(obj.password)
            obj.save()


admin.site.register(Realm, RealmAdmin)
admin.site.register(RealmSession)
