"""Declares :class:`DefaultKeystore`."""
import copy

import ioc.loader
from unimatrix.conf import settings

from .abstractkeystore import AbstractKeystore


class DefaultKeystore(AbstractKeystore):
    """A :class:`AbstractKeystore` implementation that uses the application
    settings to select a key from a mapping, based on the key identifier.

    An example configuration is provided below:

    .. code:: python

        CRYPTO_KEYSTORE = {
            "some-random-id-1": {
                "backend": "unimatrix.ext.crypto.backends.google.AsymmetricKey",
                "options": {
                    'project': "myproject",
                    'location': "europe-west4",
                    'keyring': "mykeyring",
                    'key': "mykey",
                    'version': 1
                }
            }
        }
    """
    __module__ = 'unimatrix.ext.crypto'

    def __init__(self):
        self.__keys = ...

    def _load_keys(self):
        keys = getattr(settings, 'CRYPTO_KEYSTORE', [])
        self.__keys = {}
        for kid, config in copy.deepcopy(keys):
            Key = ioc.loader.import_symbol(config['backend'])
            self.__keys[kid] = Key(config['options'], keyid=kid)

    async def get(self, keyid):
        """Lookup the key identified by `keyid`. If `keyid` is ``None``, return
        the :term:`Application Secret Key`.
        """
        if self.__keys == ...:
            self._load_keys()
        if keyid is None:
            return get_secret_key()
