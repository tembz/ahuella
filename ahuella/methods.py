from typing import Dict, Any, List, Union
from .bases import FinalCaptcha, FinalGetSticker, FinalGetStickers
from aiohttp import FormData
from .tools import Validate
from .hellahttp import Client, api_url


class JsonResponse:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Union[str, int, List[Dict[str, Any]]]:
        if name in self._data:
            value = self._data[name]

            if isinstance(value, dict):
                return JsonResponse(value)
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                return [JsonResponse(item) for item in value]

            return value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    def __str__(self):
        return str(self._data)




class HAPI():
    def __init__(self, validator: Validate):
        self.token = validator.split(':')[0]
        self.v = validator.split(':')[1]
        
    def add_param(self, params: dict) -> dict:
        params['access_token'] = self.token
        params['v'] = self.v
        del params['self']
        return params
    
    async def get_stickers(self, user_id: int | str) -> FinalGetStickers:
        params = self.add_param(locals())
        response = await Client().request_json(url=api_url + "getStickers", params=params)
        sort = JsonResponse(response)
        return sort

    async def get_groups(self, user_id: int | str) -> Exception:
        """Method not available as of 11/16/23"""
        params = self.add_param(locals())
        response = await Client().request_json(url=api_url + "getGroups", params=params)
        sort = JsonResponse(response)
        return sort
    
    async def get_sticker(self, sticker_id: int,  product_id: int ) -> FinalGetSticker:
        params = self.add_param(locals())
        response = await Client().request_json(url=api_url + "getSticker", params=params)
        sort = JsonResponse(response)
        return sort
    
    async def generation_tts(self, text: str, speaker: int = 1) -> bytes:
        """Only russian text"""
        params = self.add_param(locals())
        response = await Client().request_content(url=api_url + "GenerationTTS", params=params)
        return response				
	
    async def solve_captcha(self, sid: int) -> FinalCaptcha:
        params = self.add_param(locals())
        response = await Client().request_json(url=api_url + "solveCaptcha", params=params)
        sort = JsonResponse(response)
        return sort
    
    async def generation_quotes(self,
                              ava: str,
                              member_id: int,
                              screen_name: str,
                              name: str,
                              background_number: int = 1,
                              sticker: str | None = None,
                              sticker_id: int | None = None,
                              background: str | None = None,
                              text: str | None = None):
        """the sticker parameter is only for version 1. a link to the sticker is sent"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        params["access_token"] = self.token
        params["v"] = self.v
        data = FormData()
        if 'sticker' in params:
            sticker = params['sticker']
            sticker_get = await Client().request_content(url = sticker)
            data.add_field('sticker_bytes', sticker_get, filename='meow.jpg')
        if 'background' in params:
            back = params['background']
            back_get = await Client().request_content(url = back)
            data.add_field('background_bytes', back_get, filename='background.jpg')			
        ava = params['ava']
        ava_get = await Client().request_content(url = ava)
        del params["ava"]
        data.add_field('ava_bytes', ava_get, filename='ava.jpg')
        generation = await Client().request_quote(url = api_url+"GenerationQuotes", params=params, data=data)
        return generation
