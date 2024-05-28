import os

import requests
from .countries import CountryCodes
from dotenv import load_dotenv

import json

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)


class FacebookAPI:
	"""
	Class to interact with the Facebook Ads API.
	"""

	def __init__(self) -> None:
		"""
		Constructor to initialize the access key and the Facebook ads api endpoint.
		"""

		self.access_key = None
		self.ads_api_endpoint = "https://graph.facebook.com/v19.0/ads_archive"

	def get_access_key(self) -> str:
		"""
		Method to get the access key.

		Returns:
			str: The access key.
		"""

		self.access_key = os.getenv("FACEBOOK_ACCESS_KEY")

		return self.access_key

	def get_ads(self, search_term: str, country: str = CountryCodes.US) -> dict:
		"""
		Method to get the ads from the Facebook Ads API.

		Args:
			search_term (str): The search term.
			country (str): The country.

		Returns:
			dict: The JSON response from the API endpoint (containing the ads data).
		"""

		token_key = self.get_access_key()
		if token_key is None:
			return token_key

		params = {
			"ad_reached_countries": [country],
			"search_terms": search_term,
			# "limit": 1,
			"access_token": token_key
		}

		response = requests.get(self.ads_api_endpoint, params=params)

		store_resp = response.json()

		with open('fb_ads.json', 'w') as f:
			json.dump(store_resp, f)

		return store_resp

# print(FacebookAPI().get_ads("cat", CountryCodes.US))