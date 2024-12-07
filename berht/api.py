from typing import Optional, Union

from dacite import from_dict

from .http import Http, FormData
from .models import Groups, Sticker, Stickers, Captcha

api_url = "https://api.berht.dev/method/"

class Berht:

    def __init__(self, *,
                 token: Optional[str] = None):
        self.token = token
        self.base_params = {"token": self.token, "v": 2}
        self.http = Http()
    
    def sort_data(self, parameters: dict) -> dict:
        params = parameters | self.base_params
        return {k: v for k, v in params.items() if k != "self" and v is not None}
    
    async def request(self, method: str, params: dict):
        params = self.sort_data(params)
        response = await self.http.request_json(url=api_url+method, params=params)
        if not response["ok"]:
            raise Exception(f"API returned error: {response['error_code']} | {response['error_description']}")
        return response["object"]

    async def get_stickers(self, user_id: int) -> Stickers:
        response = await self.request("getStickers", locals())
        return from_dict(Stickers, response)
    
    async def get_sticker(self, sticker_id: int,  product_id: int) -> Sticker:
        response = await self.request("getSticker", locals())
        return from_dict(Sticker, response)
    
    async def get_groups(self, user_id: int | str) -> Groups:
        response = await self.request("getGroups", locals())
        return from_dict(Groups, response)
    
    async def solve_captcha(self, sid: int) -> Captcha:
        response = await self.request("SolveCaptcha", locals())
        return from_dict(Captcha, response)

    async def generation_tts(self, text: str, speaker: int = 1):
        response = await self.http.request_bytes(api_url+"GenerationTTS", params=self.sort_data(locals()))
        return response

    async def generation_quotes(self, ava: Union[str, bytes], member_id: int, screen_name: str, name: str, background_number: int = 1, sticker: Optional[str] = None, background: Optional[Union[str, bytes]] = None, text: Optional[str] = None):
        params = self.sort_data(locals())
        data = FormData()
        
        if background:
            if isinstance(background, str):
               bg = await self.http.request_bytes(background)
            del params["background"]
            data.add_field('background_bytes', bg, filename='background_bytes.png')
        
        if ava:
            ava = await self.http.request_bytes(ava)
        del params["ava"]
        data.add_field("ava_bytes", ava, filename="ava_bytes.png")
        response = await self.http.request_bytes(url=api_url+"GenerationQuotes", method="POST", params=params, data=data)
        return response