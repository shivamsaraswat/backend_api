import os
import urllib.parse

import requests
from .countries import CountryCodes
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)


class DateRange:
    """
    Class to represent the date range.
    """

    def __init__(self, min: str, max: str) -> None:
        """
        Constructor to initialize the date range.

        Args:
            min (str): The minimum date.
            max (str): The maximum date.
        """

        self.min = min
        self.max = max


class TikTokAPI:
    """
    Class to interact with the TikTok Ads API.
    """

    def __init__(self) -> None:
        """
        Constructor to initialize the access token and the API root.
        """

        self.access_token = None
        self.api_root = "https://open.tiktokapis.com/v2"

    def get_access_token(self) -> dict:
        """
        Method to get the access token.

        Returns:
            dict: The JSON response from the API endpoint (containing the access token).
        """

        params = {
            "client_key": os.getenv("TIKTOK_CLIENT_KEY"),
            "client_secret": os.getenv("TIKTOK_CLIENT_SECRET"),
            "grant_type": "client_credentials"
        }

        query_param = urllib.parse.urlencode(params)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(f"{self.api_root}/oauth/token/", data=query_param, headers=headers)

        response_data = response.json()
        if response_data.get("access_token", None):
            self.access_token = response_data["access_token"]

        return response_data

    def get_ads(
            self,
            search_term: str,
            country: str = CountryCodes.IT,
            ad_published_date_range: DateRange = DateRange("20230102","20230109")
        ) -> dict:
        """
        Method to get the ads from the TikTok Ads API.

        Args:
            search_term (str): The search term.
            country (str): The country (default is US).
            ad_published_date_range (DateRange): The date range.

        Returns:
            dict: The JSON response from the API endpoint (containing the TikTok ads data).
        """

        token_response = self.get_access_token()
        if token_response.get("error", None):
            return token_response

        api_endpoint = f"{self.api_root}/research/adlib/ad/query/"

        data_filters = {
            "filters": {
            "ad_published_date_range": {
                "min": ad_published_date_range.min,
                "max": ad_published_date_range.max
            },
            "country_code": country
            },
            "search_term": search_term
        }

        params = {
            "fields": "ad.id,ad.reach,ad.videos,advertiser.business_name,ad.image_urls"
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token_response['access_token']}"
        }

        try:
            response = requests.post(
                api_endpoint,
                params = params,
                headers = headers,
                data=data_filters
            )

        except requests.exceptions.RequestException as e:
            return {
                "error": "An error occurred while making the request.",
                "details": str(e)
            }

        return response.json()

# print(TikTokAPI().get_ads("cats"))
