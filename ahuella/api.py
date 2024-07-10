from abc import abstractmethod, ABC

from .aiohttp import AiohttpSession
from .exceptions import HError

API_URL = "https://api.hella.team/method/"


class ABCHella(ABC):
    def __init__(
        self,
        v: int = 2,
        token: str | None = None,
    ) -> None:
        
        self.v = v
        self.token = token
        self.session = AiohttpSession()
        self.base_params = {"v": self.v} if not self.token else {"access_token": self.token, "v": self.v}
        self.api_url = API_URL
        if str(self.v) not in ["1","2"]:
            raise HError("unsupported v")
        
    async def request(self, method: str, params: dict = {}):
        params = self.sort_data(params)
        response = await self.session.request_json(url=API_URL+method, params={**params, **self.base_params})
        if not response["ok"]:
            raise HError(f"{response['error_code']}: {response['error_description']}")
        return response["object"]

    def sort_data(self, params: dict) -> dict:
        return {k: v for k, v in params.items() if k != "self" and v is not None}
    
    @abstractmethod
    async def get_stickers(self, user_id: int | str): ...

    @abstractmethod
    async def get_sticker(self, sticker_id: int,  product_id: int): ...

    @abstractmethod
    async def get_groups(self, user_id: int | str): ...

    @abstractmethod
    async def generation_tts(self, text: str, speaker: int = 1): ...

    @abstractmethod
    async def solve_captcha(self, sid: int): ...

    @abstractmethod
    async def generation_quotes(self, ava: bytes | str, member_id: int, screen_name: str, name: str, background_number: int = 1, sticker: bytes | str | None = None, background: bytes | str | None = None, text: str | None = None): ...
       