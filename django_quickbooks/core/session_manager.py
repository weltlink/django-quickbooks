from django_quickbooks import get_realm_session_model, get_realm_model, get_qbd_task_model

Realm = get_realm_model()
RealmSession = get_realm_session_model()
QBDTask = get_qbd_task_model()


class BaseSessionManager:

    def __init__(self, **kwargs):
        super(BaseSessionManager, self).__init__(**kwargs)

    def authenticate(self, username: str, password: str) -> Realm:
        raise NotImplemented

    def create_session(self, realm: Realm) -> str:
        raise NotImplemented

    def in_session(self, realm: Realm) -> bool:
        raise NotImplemented

    def add_new_requests(self, realm: Realm):
        raise NotImplemented

    def new_requests_count(self, realm: Realm) -> int:
        raise NotImplemented

    def process_response(self, ticket: str, response: str, hresult: str, message: str) -> int:
        raise NotImplemented

    def get_request(self, realm: Realm) -> str:
        raise NotImplemented

    def close_session(self, realm: Realm):
        raise NotImplemented

    def get_realm(self, ticket: str) -> Realm:
        raise NotImplemented

    def put_request(self, request: str, realm: Realm):
        raise NotImplemented

    def check_iterating_request(self, request: str, ticket: str):
        raise NotImplemented

    def is_iterating_request(self, request: str) -> bool:
        raise NotImplemented
