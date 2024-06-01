from fastapi import HTTPException, status

from ads_apis.facebook import FacebookAPI
from ads_apis.tiktok import TikTokAPI
from repositories.UserRepository import UserRepository
import requests


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
    
    def test_facebook_ads(self,search_term, country) -> dict:
        ads = self.facebook_ads_api.get_ads(search_term,country)
        for ad in ads["data"]:
            response = requests.get(ad["ad_snapshot_url"])
            tokens = str(response.content).split('"')
            try:
                index = tokens.index("video_sd_url")
            except ValueError as e:
                print(e)
                ad["video_url"] = None
            else:
                overslashed = tokens[index+2]
                slashedIterable = overslashed.split("\\")
                slashed = "".join(slashedIterable)
                ad["video_url"] = slashed
        return ads
    
    def test_data(self) -> dict:
        return {
            "data": [
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=385550857686219&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-09",
                    "id": "385550857686219",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435550444_844646174089476_7552876420705272671_n.mp4?_nc_cat=106&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=F_3Re_qSWdAQ7kNvgGH8-cj&_nc_ht=video.flun3-1.fna&oh=00_AYDebH4xgmqncY41hoUy4dzOQRV3FCSkk1BWoStugH1tUg&oe=665FAB90"
                },
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=414618577827001&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-08",
                    "id": "414618577827001",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435524395_1166596594366366_1533313759189188165_n.mp4?_nc_cat=107&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=nx2-A85oniMQ7kNvgFXXMQA&_nc_ht=video.flun3-1.fna&oh=00_AYCB0nwPIGfNPHP1FDEzS0sQfApFLVQtIHfICXopCmA6NQ&oe=665FD279"
                },
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=1007632497616908&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-08",
                    "id": "1007632497616908",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435422449_299677773158648_4493581817073448756_n.mp4?_nc_cat=103&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=IBJ4yo29lbIQ7kNvgGgIIUV&_nc_ht=video.flun3-1.fna&oh=00_AYDQYdDHeh_onPOKlUlHb3iMVw2zozeU7nN3pcZRdg7UjQ&oe=665FB934"
                },
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=1211570793141331&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-08",
                    "id": "1211570793141331",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435419876_1573779886768661_7524472440022483450_n.mp4?_nc_cat=108&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=Gqkeo3JydU8Q7kNvgFS_kNG&_nc_ht=video.flun3-1.fna&oh=00_AYAYOBOtJYwevQIidqSduWMZS9qlR9xSsIdgcTfoyhOaqg&oe=665FC9D4"
                },
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=1446205086267878&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-09",
                    "id": "1446205086267878",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435585214_7357556187656586_4454265796936444819_n.mp4?_nc_cat=107&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=mlej_oBMpcgQ7kNvgFT7fYV&_nc_ht=video.flun3-1.fna&oh=00_AYCArK5Kn4-beUaVM9npG5wjC90qm4uGHCSGyQfdrGuW-A&oe=665FC238"
                },
                {
                    "page_id": "100814379735109",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=3355500181409212&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-04-08",
                    "ad_delivery_stop_time": "2024-04-08",
                    "id": "3355500181409212",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/435676088_1555187845056663_8807101496007930953_n.mp4?_nc_cat=108&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=hW9cD9xEWFwQ7kNvgED2RTW&_nc_ht=video.flun3-1.fna&oh=00_AYDgG0ejhQm9EK4nPCWEWDK2zABhktbxzGBgOS26FP9oyA&oe=665FA503"
                },
                {
                    "page_id": "107875349019583",
                    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=7846460848748695&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP",
                    "ad_delivery_start_time": "2024-05-30",
                    "id": "7846460848748695",
                    "video_url": "https://video.flun3-1.fna.fbcdn.net/v/t42.1790-2/447069788_502970628730602_8071361414998278320_n.mp4?_nc_cat=100&ccb=1-7&_nc_sid=c53f8f&_nc_ohc=43gAqqPAe9kQ7kNvgF1sEZI&_nc_ht=video.flun3-1.fna&oh=00_AYA_Q1P19TtcdsMgOMHZNtpQ66heeu9OvhOoK-M2tiHMZQ&oe=665F9F9A"
                },
            ],
            "paging": {
                "cursors": {
                    "after": "c2NyYXBpbmdfY3Vyc29yOk1UY3hOekEyTkRFM056b3hNak14TkRJeU1UVTRNalkyT0RZAMQZDZD"
                },
                "next": "https://graph.facebook.com/v19.0/ads_archive?ad_reached_countries=us&search_terms=dropshipping&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP&limit=25&after=c2NyYXBpbmdfY3Vyc29yOk1UY3hOekEyTkRFM056b3hNak14TkRJeU1UVTRNalkyT0RZAMQZDZD"
            }
        }
    
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
