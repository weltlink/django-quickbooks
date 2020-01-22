from abc import abstractmethod

from django_quickbooks import get_realm_session_model, get_realm_model, get_qbd_task_model

Realm = get_realm_model()
RealmSession = get_realm_session_model()
QBDTask = get_qbd_task_model()


class BaseSessionManager:

    @abstractmethod
    def authenticate(self, username: str, password: str) -> Realm:
        pass

    @abstractmethod
    def set_ticket(self, realm: Realm) -> str:
        pass

    @abstractmethod
    def in_session(self, realm: Realm) -> bool:
        pass

    @abstractmethod
    def add_new_jobs(self, realm: Realm) -> None:
        pass

    @abstractmethod
    def new_jobs(self, realm: Realm) -> int:
        pass

    @abstractmethod
    def process_response(self, ticket: str, response: str, hresult: str, message: str) -> int:
        pass

    @abstractmethod
    def get_request(self, ticket: str) -> str:
        pass

    @abstractmethod
    def clear_ticket(self, ticket: str) -> str:
        pass
