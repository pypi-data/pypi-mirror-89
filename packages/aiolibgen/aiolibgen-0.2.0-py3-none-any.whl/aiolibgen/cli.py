import fire
from aiokit.utils import sync_fu
from aiolibgen.client import LibgenClient


async def books(base_url, ids):
    async with LibgenClient(base_url=base_url) as c:
        return await c.by_ids(ids)


def main():
    fire.Fire(sync_fu(books))


if __name__ == '__main__':
    main()
