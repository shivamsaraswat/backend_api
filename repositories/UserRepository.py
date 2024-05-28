import datetime as dt
import os
from datetime import datetime, timedelta
from typing import Any

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import PyJWTError
from passlib.context import CryptContext
from passlib.hash import bcrypt
from password_strength import PasswordStats

from DTOs.user import ActiveSession, LoginSchema, User
from entity_manager.entity_manager import entity_manager
from repositories.IUserRepository import IUserRepository

# Load the environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

# CryptContext for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(IUserRepository):
    """
    This class is responsible for handling all the operations related to the user collection in the database.
    """

    def __init__(self) -> None:
        """
        The constructor initializes the entity manager for the user collection and the active sessions collection.
        """

        self.em = entity_manager.get_collection(os.environ.get("USER_COLLECTION"))
        self.activeSessionsEntityManager = entity_manager.get_collection(os.environ.get("ACTIVE_SESSIONS_COLLECTION"))


    def register(self, user: User) -> Any:
        """
        This method is responsible for registering a new user in the database.

        Args:
            user (User): The user object.

        Returns:
            User: The user object if the user is registered successfully.
            bool: False if the user already exists.
        """

        # Check if the email is already present in the database
        is_email_already_present = self.em.find_one({"email": user.email})

        # Check if the password is strong enough
        is_password_strong = self.is_password_strong(user.password.get_secret_value())

        # If the email is not present and the password is strong, register the user
        if is_email_already_present is None and is_password_strong:
            self.em.insert_one(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "password": bcrypt.using(rounds=12).hash(user.password.get_secret_value()),
                    "referral_code": user.referral_code,
                }
            )
            return user

        else:
            return False


    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        """
        This method is responsible for creating an access token.

        Args:
            data (dict): The data to be encoded in the token.
            expires_delta (timedelta): The expiry time of the token.

        Returns:
            str: The encoded JWT token.
        """

        to_encode = data.copy()
        expire = datetime.now(dt.UTC) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
        return encoded_jwt


    def get_user(self, email: str) -> Any:
        """
        This method is responsible for getting the user from the database.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user object if the user exists.
            None: None if the user does not exist.
        """

        # Get the user from the database
        usr = self.em.find_one({"email": email})

        # If the user exists, return the user object
        if usr is not None:
            return LoginSchema(
                email = usr["email"],
                password = usr["password"]
            )
        else:
            # If the user does not exist, raise an exception
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user credentials.", headers={"WWW-Authenticate": "Bearer"})


    def is_password_correct(self, form_data: LoginSchema) -> bool:
        """
        This method is responsible for checking if the password is correct.

        Args:
            form_data: The form data containing the user email and password.

        Returns:
            bool: True if the password is correct, False otherwise.
        """

        # Get the user from the database
        user = self.get_user(form_data.email)

        # Check if the password is correct or not
        if user is None or not pwd_context.verify(form_data.password.get_secret_value(), user.password.get_secret_value()):
            return False

        return True


    def is_password_strong(self, password: str) -> bool:
        """
        This method is responsible for checking if the password is strong.

        Args:
            password (str): The password.

        Returns:
            bool: True if the password is strong enough, False otherwise.
        """

        # Check if the password is strong or not, by checking the complexity of the password
        if PasswordStats(password).strength() >= 0.66:
            return True

        return False


    def get_access_token(self, form_data: LoginSchema) -> str:
        """
        This method is responsible for getting the access token.

        Args:
            form_data: The form data containing the user email and password.

        Returns:
            str: The access token.
        """

        # Access token expiry time
        access_token_expiry_time = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))

        # Create the access token and return it
        access_token = self.create_access_token(
            data={"sub": form_data.email}, expires_delta=access_token_expiry_time
        )
        return access_token


    def authenticate(self, token: str) -> None:
        """
        This method is responsible for authenticating the user.

        Args:
            token (str): The token.
        """

        try:
            # Decode the token
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])

            # Get the email from the token
            email: str = payload.get("sub")

            # Check if the email is None
            if email is None:
                raise HTTPException(status_code=400, detail="Could not validate credentials, user not found.")

            # Check if the token has expired
            expiry_time = payload.get("exp")
            if expiry_time is None or expiry_time < datetime.now().timestamp():
                self.activeSessionsEntityManager.delete_many({"email": email})
                raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")

            # Check if the email exists in the active sessions
            session = self.activeSessionsEntityManager.find_one({"email": email})
            if not session:
                raise HTTPException(status_code=401, detail="User session not found.")

        except PyJWTError:
            # If there is an error in decoding the token, raise an exception
            raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")


    def register_token_in_session(self, token: str) -> None:
        """
        This method is responsible for registering the token in the active sessions.

        Args:
            token (str): The token.
        """

        try:
            # Decode the token
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])

            # Get the email and expiry time from the token
            user_email, expiration_time = payload.get("sub"), payload.get("exp")
            expiration_datetime = datetime.fromtimestamp(expiration_time)

            # Create a new active session
            new_active_session = ActiveSession(
                email=user_email,
                access_token=token,
                expiry_time=expiration_datetime
            )

            # Insert the active session in the database
            self.activeSessionsEntityManager.insert_one(new_active_session.model_dump())

        except PyJWTError:
            # If there is an error in decoding the token, raise an exception
            raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")


    def logout(self, token:str) -> None:
        """
        This method is responsible for logging out the user.

        Args:
            token (str): The token.
        """

        # Delete the session from the active sessions
        self.activeSessionsEntityManager.delete_many({"access_token": token})


    def is_session_active(self, email: str) -> bool:
        """
        This method is responsible for checking if the session is active.

        Args:
            email (str): The email.

        Returns:
            bool: True if the session is active.
            bool: False if the session is not active.
        """

        # First, check if the user has an active session
        existing_session = self.activeSessionsEntityManager.find_one({"email": email})
        if not existing_session: return False

        # If an active session exists, check if the token is still valid
        try:
            # Decode the token
            payload = jwt.decode(existing_session["access_token"], os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])

            # Get the expiry time and current time
            expiry_time = payload.get("exp")
            current_time = datetime.now().timestamp()

            if expiry_time is None or expiry_time < current_time:
                # Token has expired
                self.activeSessionsEntityManager.delete_many({"email": email})
                return False

        except PyJWTError:
            # There was an error in processing the token, delete the session and return false as session is no longer active.
            self.activeSessionsEntityManager.delete_many({"email": email})
            return False

        return True


    def get_access_token_from_active_session(self, email: str) -> str:
        """
        This method is responsible for getting the access token from the active session.

        Args:
            email (str): The email.

        Returns:
            str: The access token.
        """

        # Check if the user has an active session
        existing_session = self.activeSessionsEntityManager.find_one({"email": email})

        # If the user has an active session, return the access token
        if existing_session is not None: return existing_session["access_token"]

        # If the user does not have an active session, return None
        return None
