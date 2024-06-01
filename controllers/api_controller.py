from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from services.api_service import ApiService

api_controller_router = InferringRouter()


@cbv(api_controller_router)
class ApiController:
    """
    Class to handle the API requests for the Ads APIs
    """

    def __init__(self) -> None:
        """
        Constructor to initialize the ApiService object.
        """

        self.api_service = ApiService()

    @api_controller_router.post("/facebook_ads")
    def facebook_ads(self, email: str, search_term: str = "dropshipping", country: str = "us") -> dict:
        """
        Method to get the ads from the Facebook Ads API.

        Args:
            email (str): The email of the user.
            country (str): The country name to filter the ads.
            search_term (str): The search term.

        Returns:
            dict: The JSON response from the API endpoint (containing the Facebook ads data).
        """

        try:
            return self.api_service.facebook_ads(email, search_term, country)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    @api_controller_router.get("/test_facebook_ads")
    def test_facebook_ads(self, search_term: str = "dropshipping", country: str = "us")->dict:
        return self.api_service.test_facebook_ads(search_term,country)
    
    @api_controller_router.get("/test_data")
    def test_facebook_ads(self)->dict:
        return self.api_service.test_data()

    @api_controller_router.post("/tiktok_ads")
    def tiktok_ads(self, email: str, search_term: str = "dropshipping", country: str = "us") -> dict:
        """
        Method to get the ads from the TikTok Ads API.

        Args:
            email (str): The email of the user.
            country (str): The country name to filter the ads.
            search_term (str): The search term.

        Returns:
            dict: The JSON response from the API endpoint (containing the TikTok ads data).
        """

        try:
            return self.api_service.tiktok_ads(email, search_term, country)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
