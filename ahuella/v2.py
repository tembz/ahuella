from dacite import from_dict

from .api import ABCHella
from .models import v2


class HellaApiv2(ABCHella):
    
    def __init__(self, token: str | None = None) -> None:
        super().__init__(2, token)

    async def get_stickers(self, user_id: int | str) -> v2.Stickers:
        response = await self.request("getStickers", locals())
        return from_dict(v2.Stickers, response)


    async def get_sticker(self, sticker_id: int, product_id: int) -> v2.Sticker:
        response = await self.request("getSticker", locals())
        return from_dict(v2.Sticker, response)
    

    async def get_groups(self, user_id: int | str) -> v2.Groups:
        response = await self.request("getGroups", locals())
        return from_dict(v2.Groups, response)


    async def solve_captcha(self, sid: int) -> v2.Captcha:
        response = await self.request("SolveCaptcha", locals())
        return from_dict(v2.Captcha, response)
    

    async def generation_tts(self, text: str, speaker: int = 1) -> bytes:
        response = await self.session.request_bytes(self.api_url+"GenerationTTS", params=self.sort_data(locals()))
        return response

    async def generation_quotes(self, ava: bytes | str, member_id: int, screen_name: str, name: str, background_number: int = 1, sticker: bytes | str | None = None, background: bytes | str | None = None, text: str | None = None) -> bytes:
        ...