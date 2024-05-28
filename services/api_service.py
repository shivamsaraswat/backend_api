from fastapi import HTTPException, status

from ads_apis.facebook import FacebookAPI
from ads_apis.tiktok import TikTokAPI
from repositories.UserRepository import UserRepository


class ApiService:
    """
    This class is responsible for handling all the operations related to the user collection in the database.
    """

    def __init__(self) -> None:
        """
        The constructor initializes the user repository.
        """

        self.facebook_ads_api = FacebookAPI()
        self.tiktok_ads_api = TikTokAPI()
        self.user_repository = UserRepository()

    def facebook_ads(self, email: str, search_term: str = "dropshipping", country: str = "us") -> dict:
        """
        This method is responsible for fetching the Facebook ads data based on the search term and country.

        Args:
            email (str): The email of the user.
            search_term (str): The search term for the ads.
            country (str): The country name to filter the ads.

        Returns:
            dict: The JSON response from the API endpoint (containing the Facebook ads data).
        """

        is_session_active = self.user_repository.is_session_active(email)

        if not is_session_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is not active.")

        return self.facebook_ads_api.get_ads(search_term, country)
    
    def tiktok_ads(self, email: str, search_term: str = "dropshipping", country: str = "us") -> dict:
        """
        This method is responsible for fetching the TikTok ads data based on the search term and country.

        Args:
            email (str): The email of the user.
            search_term (str): The search term for the ads.
            country (str): The country name to filter the ads.

        Returns:
            dict: The JSON response from the API endpoint (containing the TikTok ads data).
        """

        is_session_active = self.user_repository.is_session_active(email)

        if not is_session_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session is not active.")

        return self.tiktok_ads_api.get_ads(search_term, country)
