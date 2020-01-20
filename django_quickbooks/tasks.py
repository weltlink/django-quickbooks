from celery.task import task

from django_quickbooks.request_builder import RequestBuilder


@task
def build_request(request_body, realm_id):
    RequestBuilder().process(realm_id, request_body)
