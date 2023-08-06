from aiobaseclient.exceptions import (
    ClientError,
    ExternalServiceError,
    NotFoundError,
    TemporaryError,
)


class ExceededConnectionsError(TemporaryError):
    pass


__all__ = [
    'ClientError', 'ExternalServiceError', 'NotFoundError', 'ExceededConnectionsError',
]
