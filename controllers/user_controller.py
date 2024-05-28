from typing import Any

from fastapi import Header, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from DTOs.CustomResponseMessage import CustomResponseMessage
from DTOs.user import LoginSchema, User
from services.user_service import UserService

user_controller_router = InferringRouter()


@cbv(user_controller_router)
class UserController:
    """
    This class is responsible for handling all the operations related to the user collection in the database.
    """

    def __init__(self) -> None:
        """
        The constructor initializes the user service.
        """

        self.user_service = UserService()


    @user_controller_router.post("/register")
    def register(self, user: User) -> Any:
        """
        This method is responsible for registering a new user in the database.

        Args:
            user (User): The user object.

        Returns:
            CustomResponseMessage or HTTPException: The response message if the user is registered successfully or an HTTPException if their is an error.
        """

        try:
            # Register the user and get the response
            usr = self.user_service.register(user)

            # Check if the user is registered successfully or not
            if usr is not False:
                return CustomResponseMessage(status_code=status.HTTP_200_OK, message=f"User {user.email} registered successfully.")
            else:
                # Raise an exception if the user already exists or the password is not strong enough
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User already exists or password is not strong enough.")

        except Exception as e:
            # Raise an exception if there is an error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    @user_controller_router.post("/login")
    def login(self, form_data: LoginSchema) -> dict:
        """
        This method is responsible for logging in a user and generating an access token for them.

        Args:
            form_data: The form data containing the user email and password.

        Returns:
            dict: The access token and the token type.
        """

        try:
            # Get the access token from the user service
            access_token = self.user_service.get_access_token(form_data)

            # Check if the access token is None and raise an exception
            if access_token["access_token"] is None:
                raise HTTPException(status_code=400, detail="Incorrect email or password")

            return access_token

        except Exception as e:
            # Raise an exception if there is an error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    @user_controller_router.post("/logout")
    def logout(self, token: str = Header(None)) -> Any:
        """
        This method is responsible for logging out a user.

        Args:
            token (str): The access token of the user.

        Returns:
            CustomResponseMessage or HTTPException: The response message if the user is logged out successfully or an HTTPException if their is an error.
        """

        try:
            # Check if the token is None and raise an exception
            if token is None: raise HTTPException(status_code=401, detail="Invalid token")

            # Log out the user and get the response
            self.user_service.logout(token)
            return CustomResponseMessage(status_code=200, message="Logged out successfully")

        except Exception as e:
            # Raise an exception if there is an error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
