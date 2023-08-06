"""Declares :class:`AbstractKeystore`."""
from unimatrix.conf import settings

from .secret import get_secret_key


class AbstractKeystore:
    """The base class for all :term:`Key Store` implementations. A Key Store
    provides an interface to lookup private or public keys.
    """

    async def get(self, keyid):
        raise NotImplementedError
