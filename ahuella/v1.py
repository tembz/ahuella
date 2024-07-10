from dacite import from_dict

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
        ...


    