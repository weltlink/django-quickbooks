from django.db import models


class ExternalItemServiceManager(models.QuerySet):
    def set(self, item_service, external_item_service_ids, realm_id):
        self.filter(
            external_item_service_id__in=external_item_service_ids,
            item_service__realm_id=realm_id
        ).delete()

        self.bulk_create(
            [self.model(item_service=item_service, external_item_service_id=external_item_service_id)
             for external_item_service_id in external_item_service_ids]
        )
