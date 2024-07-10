## Асинхронный типизированный модуль для работы с api.hella.team

```python
import asyncio

from ahuella.v2 import HellaApiv2 #class for API version 2

hella = HellaApiv2("YOU TOKEN")


async def first_request():
  stickers = await hella.get_stickers(user_id=1)
  print(stickers.items.free.count)
  # >>> 50

asyncio.run(first_request())
```

## Установка
```shell
pip install ahuella
```
