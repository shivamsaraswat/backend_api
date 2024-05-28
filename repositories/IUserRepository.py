from abc import abstractmethod
from datetime import timedelta

from DTOs.user import LoginSchema, User


class IUserRepository:
    @abstractmethod
    def register(self, user : User) -> User: pass

    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: timedelta): pass

    @abstractmethod
    def get_user(self, email: str): pass

    @abstractmethod
    def get_access_token(self, form_data: LoginSchema): pass

    @abstractmethod
    def authenticate(self, token: str): pass

    @abstractmethod
    def is_password_correct(self, form_data: LoginSchema) -> bool: pass

    @abstractmethod
    def register_token_in_session(self, token: str): pass

    @abstractmethod
    def logout(self, token: str): pass

    @abstractmethod
    def is_session_active(self, email: str): pass

    @abstractmethod
    def get_access_token_from_active_session(self, email: str): pass
