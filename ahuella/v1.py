from dacite import from_dict

from .aiohttp import FormData
from .api import ABCHella
from .models import v1


class HellaApiv1(ABCHella):
    
    def __init__(self, token: str | None = None) -> None:
        super().__init__(1, token)

    async def get_stickers(self, user_id: int | str) -> v1.Stickers:
        response = await self.request("getStickers", locals())
        return from_dict(v1.Stickers, response)


    async def get_sticker(self, sticker_id: int, product_id: int) -> v1.Sticker:
        response = await self.request("getSticker", locals())
        return from_dict(v1.Sticker, response)
    

    async def get_groups(self, user_id: int | str) -> v1.Groups:
        response = await self.request("getGroups", locals())
        return from_dict(v1.Groups, response)


    async def solve_captcha(self, sid: int) -> v1.Captcha:
        response = await self.request("SolveCaptcha", locals())
        return from_dict(v1.Captcha, response)
    

    async def generation_tts(self, text: str, speaker: int = 1) -> bytes:
        response = await self.session.request_bytes(self.api_url+"GenerationTTS", params=self.sort_data(locals()))
        return response

    async def generation_quotes(self, ava: bytes | str, member_id: int, screen_name: str, name: str, background_number: int = 1, sticker: bytes | str | None = None, background: bytes | str | None = None, text: str | None = None) -> bytes:
        sorted_params = self.sort_data(locals())
        params = {**sorted_params, **self.params}
        data = FormData()

        if sticker:
            if isinstance(sticker, str):
                sticker = await self.session.request_bytes(sticker)
            data.add_field('sticker_bytes', sticker, filename='sticker_bytes.png')
            del params["sticker"]
        if background:
            if isinstance(background, str):
                background = await self.session.request_bytes(background)
            del params["background"]
            data.add_field('background_bytes', background, filename='background_bytes.png')

        if isinstance(ava, str):
            ava = await self.session.request_bytes(ava)
        del params["ava"]
        data.add_field("ava_bytes", ava, filename="ava_bytes.png")

        response = await self.session.request_bytes(url=self.api_url+"GenerationQuotes", method="POST", params=params, data=data)
        return response


    