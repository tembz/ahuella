
import asyncio
import logging
from aiohttp import ClientResponse

versions = [1,2,'1','2']
class HError(Exception):
	pass

class Validate(str):
		
	def __new__(cls, token: str, v: int = 2) -> str | Exception:
		from .hellahttp import Client
		if v in versions:
			loop = asyncio.get_event_loop()
			is_valid = loop.run_until_complete(Client().get_token(f'https://api.hella.team/method/ping?v=1&access_token={token}'))
			if is_valid['ok'] == True:
				logging.debug(f"Validation successful! API version used - {v}")
				return super().__new__(cls, f"{token}:{v}")
			raise HError("Invalid Token!")
		raise HError("Hella not supported this version")

async def check_response(response: ClientResponse):
	status = response.status
	if status != 200:
		raise HError("request returned {} status code".format(status))
	response_parse  = await  response.json()
	if response_parse["ok"] != True:
		raise HError(f'{response_parse["error_code"]}: {response_parse["error_description"]}')
	return True


	
	
