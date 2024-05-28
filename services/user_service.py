from typing import Any

from DTOs.user import LoginSchema, User
from repositories.UserRepository import UserRepository


class UserService:
    """
    This class is responsible for handling all the operations related to the user collection in the database.
    """

    def __init__(self) -> None:
        """
        The constructor initializes the user repository.
        """

        self.user_repository = UserRepository()


    def register(self, user: User) -> Any:
        """
        This method is responsible for registering a new user in the database.

        Args:
            user (User): The user object.

        Returns:
            User: The user object if the user is registered successfully.
            bool: False if the user already exists.
        """

        return self.user_repository.register(user)


    def get_access_token(self, form_data: LoginSchema) -> dict:
        """
        This method is responsible for generating an access token for the user and registering it in the session.

        Args:
            form_data: The form data containing the user email and password.

        Returns:
            dict: The access token and the token type.
        """

        # Check if the password is correct
        if not self.user_repository.is_password_correct(form_data): return {"access_token": None, type: "bearer"}

        if not self.is_session_active(form_data.email):
            # If the session is not active, generate a new access token
            access_token = self.user_repository.get_access_token(form_data)

            if access_token is not None:
                self.register_token_in_session(access_token)

            return {"access_token": access_token, "token_type": "bearer"}

        else:
            # If the session is already active, return the active access token
            active_access_token = self.user_repository.get_access_token_from_active_session(form_data.email)
            return {"access_token": active_access_token, "token_type": "bearer"}


    def authenticate(self, token: str) -> bool:
        """
        This method is responsible for authenticating the user.

        Args:
            token (str): The access token.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """

        return self.user_repository.authenticate(token)


    def register_token_in_session(self, token: str) -> None:
        """
        This method is responsible for registering the token in the session.

        Args:
            token (str): The access token.
        """

        self.user_repository.register_token_in_session(token)


    def logout(self, token: str) -> None:
        """
        This method is responsible for logging out the user.

        Args:
            token (str): The access token.
        """

        self.user_repository.logout(token)


    def is_session_active(self, email: str) -> bool:
        """
        This method is responsible for checking if the session is active.

        Args:
            email (str): The email.

        Returns:
            bool: True if the session is active and False otherwise.
        """

        return self.user_repository.is_session_active(email)
