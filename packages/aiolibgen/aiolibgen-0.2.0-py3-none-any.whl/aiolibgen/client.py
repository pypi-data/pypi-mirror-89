from typing import (
    Dict,
    Iterable,
)

import orjson as json
from aiobaseclient import BaseClient
from aiolibgen.exceptions import (
    ClientError,
    ExceededConnectionsError,
    ExternalServiceError,
    NotFoundError,
)


class LibgenClient(BaseClient):
    default_fields = [
        'title',
        'author',
        'md5',
        'filesize',
        'descr',
        'edition',
        'extension',
        'pages',
        'series',
        'year',
        'language',
        'identifier',
        'id',
        'coverurl',
        'doi',
        'tags',
        'timelastmodified',
        'visible',
    ]

    async def by_ids(self, ids, fields=None):
        if not fields:
            fields = self.default_fields
        if not isinstance(ids, Iterable):
            ids = [ids]
        ids = list(map(str, ids))
        r = await self.get(
            '/json.php',
            params={
                'ids': ','.join(ids),
                'fields': ','.join(fields),
            }
        )
        return r

    async def newer(self, timenewer, idnewer=0, fields=None):
        if not fields:
            fields = self.default_fields
        while True:
            rows = await self.get(
                '/json.php',
                params={
                    'fields': ','.join(fields),
                    'mode': 'newer',
                    'timenewer': timenewer,
                    'idnewer': idnewer,
                }
            )
            if not rows:
                return
            for row in rows:
                timenewer = row['timelastmodified']
                idnewer = row['id']
                yield row

    async def response_processor(self, response):
        text = await response.text()
        if response.status == 404:
            raise NotFoundError(status=response.status, text=text, url=response.url)
        elif response.status == 500 and 'max_user_connections' in text:
            raise ExceededConnectionsError()
        elif response.status != 200:
            raise ExternalServiceError(response.url, response.status, text)
        data = json.loads(text)
        if isinstance(data, Dict) and 'error' in data:
            raise ClientError(**data)
        return data
