from aiohttp import ClientSession, ClientResponse, FormData

class AiohttpSession:

    async def request_raw(
            self,
            url: str,
            method: str = "GET",
            data: dict | None = None,
            **request_params
    ) -> ClientResponse:

        async with ClientSession() as session:
            response = await session.request(method=method, url=url, data=data, **request_params)
            await response.read()
            return response
        
    async def request_json(
            self,
            url: str,
            method: str = "GET",
            data: dict | None = None,
            **request_params
    ) -> dict:
        
        response = await self.request_raw(url, method, data, **request_params)
        return await response.json(encoding="utf-8")
    
    async def request_bytes(
            self,
            url: str,
            method: str = "GET",
            data: dict | None = None,
            **request_params
    ) -> bytes:
        
        response = await self.request_raw(url, method, data, **request_params)
        return response._body
        