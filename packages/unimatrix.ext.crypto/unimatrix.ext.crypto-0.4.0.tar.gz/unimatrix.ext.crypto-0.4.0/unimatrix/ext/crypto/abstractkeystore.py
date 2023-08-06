"""Declares :class:`AbstractKeystore`."""


class AbstractKeystore:
    """The base class for all :term:`Key Store` implementations. A Key Store
    provides an interface to lookup private or public keys.
    """

    @property
    def keys(self):
        return self.__keys

    def __init__(self):
        self.__keys = {}

    def register(self, keyid: str, key):
        if keyid in self.keys:
            raise ValueError(f"Key already registered: {keyid}")
        self.keys[keyid] = key

    def get(self, keyid):
        return self.keys[keyid]
