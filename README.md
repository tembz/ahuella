## Асинхронный типизированный модуль для работы с api.hella.team

```python
import asyncio

from berht import Berht

api = Berht()

async def first_request():
  stickers = await api.get_stickers(user_id=1)
  print(stickers.items.free.count)
  # >>> 54

asyncio.run(first_request())
```

## Установка
```shell
pip install ahuella
```
