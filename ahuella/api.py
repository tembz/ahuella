import asyncio

from dacite import from_dict

from .aiohttp import AiohttpSession, FormData
from .exceptions import InvalidToken, HError
from .models import Stickers, Sticker, Captcha, Groups

API_URL = "https://api.hella.team/method/"


class HellaAPI():
    def __init__(
        self,
        v: int = 2,
        token: str | None = None,
    ) -> None:
        
        """models are written for API version 2. when you try to use version 1, the dict will be given"""

        self.v = v
        self.token = token
        self.session = AiohttpSession()
        self.params = {"v": self.v} if not self.token else {"access_token": self.token, "v": self.v}
        self.api_url = API_URL

        if str(self.v) not in ["1","2"]:
            raise HError("unsupported v")

        if self.token:
            new_loop = asyncio.new_event_loop()
            is_valid = new_loop.run_until_complete(self.session.request_json(url=API_URL+"ping", params=self.params))
            if is_valid['ok'] != True:
                raise InvalidToken()
        
    async def request(self, method: str, params: dict = {}):
        params = self.sort_data(params)
        response = await self.session.request_json(url=API_URL+method, params={**params, **self.params})
        if not response["ok"]:
            raise HError(f"{response['error_code']}: {response['error_description']}")
        return response["object"]

    def sort_data(self, params: dict) -> dict:
        return {k: v for k, v in params.items() if k != "self" and v is not None}


    async def get_stickers(self, user_id: int | str) -> Stickers:
        response = await self.request("getStickers", locals())
        return from_dict(Stickers, response) if self.v == 2 else response

    async def get_sticker(self, sticker_id: int,  product_id: int) -> Sticker:
        response = await self.request("getSticker", locals())
        return from_dict(Sticker, response) if self.v == 2 else response
    
    async def get_groups(self, user_id: int | str) -> Groups:
        response = await self.request("getGroups", params=locals())
        return from_dict(Groups, response) if self.v == 2 else response

    async def generation_tts(self, text: str, speaker: int = 1) -> bytes:
        """Only russian text"""
        sorted_params = self.sort_data(locals())
        params = {**sorted_params, **self.params}
        response = await self.session.request_bytes(url=API_URL+"GenerationTTS", params=params)
        return response

    async def solve_captcha(self, sid: int) -> Captcha:
        response = await self.request("solveCaptcha", locals())
        return from_dict(Captcha, {"object": response}) if self.v == 2 else {"object": response}


    async def generation_quotes(
            self,
            ava: bytes | str,
            member_id: int,
            screen_name: str,
            name: str,
            background_number: int = 1,
            sticker: bytes | str | None = None,
            background: bytes | str | None = None,
            text: str | None = None) -> bytes:
        sorted_params = self.sort_data(locals())
        params = {**sorted_params, **self.params}
        data = FormData()
        
        if sticker:
            if isinstance(sticker, bytes) and self.v == 1:
                data.add_field('sticker_bytes', sticker, filename='sticker_bytes.png')
                del params["sticker"]

            if isinstance(sticker, bytes) and self.v == 2:
                raise TypeError("API version 2 does not support bytes in the sticker parameter, please paste the link")
            

        if background:
            if isinstance(background, str):
                background = await self.session.request_bytes(background)
            del params["background"]
            data.add_field('background_bytes', background, filename='background_bytes.png')

        if isinstance(ava, str):
            ava = await self.session.request_bytes(ava)
        del params["ava"]
        data.add_field("ava_bytes", ava, filename="ava_bytes.png")

        response = await self.session.request_bytes(url=API_URL+"GenerationQuotes", method="POST", params=params, data=data)
        return response