# aiocrossref

Asynchronous client for Libgen API

## Example

```python
import asyncio

from aiolibgen import LibgenClient

async def books(base_url, ids):
    client = LibgenClient(base_url)
    return await client.by_ids(ids)

response = asyncio.get_event_loop().run_until_complete(books('http://gen.lib.rus.ec', [100500]))
```