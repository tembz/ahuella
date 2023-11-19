from ahuella import HAPI, Validate
import asyncio

hella = HAPI(Validate("HELLA KEY"))

async def test():
    get_stickers = await hella.get_stickers(user_id=497625184)
    print(get_stickers.object.items)

asyncio.run(test())
