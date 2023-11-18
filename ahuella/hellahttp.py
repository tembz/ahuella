import aiohttp
from aiohttp import ClientSession
from .tools import check_response

Quote = "QuoteBytes"
api_url = 'https://api.hella.team/method/'

class Client():
	
	async def request_json(
		self,
		url: str,
		method: str = "GET",
		params: dict | None = None):
			async with ClientSession() as session:
				async with session.request(url=url, method=method, params=params) as request:
					check = await check_response(request)
					if check:
						return await request.json()
				
	async def request_content(
		self,
		url: str,
		params: dict | None = None) -> bytes:
			async with ClientSession() as session:
				async with session.get(url=url, params=params) as request:
					return await request.read()

	
	async def sort_param(self, params):
		return {k: v for k, v in params.items() if v is not None and k != "self"}

	async def request_quote(self, url: str, params: dict | None = None, data: aiohttp.FormData | None = None):
		async with ClientSession() as session:
			async with session.post(url=url, data=data, params=params) as response:
				return await response.read()
