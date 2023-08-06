"""Declares :class:`PrivateKey`."""
import abc

from unimatrix.lib.datastructures import ImmutableDTO


class PrivateKey(metaclass=abc.ABCMeta):
    """Provides an interface for signing and decryption
    operations.
    """
    capabilities = abc.abstractproperty()

    @property
    def metadata(self):
        return ImmutableDTO.fromdict(
            {**self.get_metadata(), 'keyid': self.__keyid})

    def __init__(self, opts, keyid=None):
        self.__keyid = keyid
        self.__opts = ImmutableDTO.fromdict(dict(opts))
        self.setup(self.__opts)

    @abc.abstractmethod
    def setup(self, opts):
        raise NotImplementedError

    def get_metadata(self) -> dict:
        return {}

    async def can_use(self, oid: str) -> bool:
        """Return a boolean if the key can use the algorithm identified by
        the provided `oid`.
        """
        return oid in self.capabilities

    async def encrypt(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the cipher text of byte-sequence `blob`."""
        raise NotImplementedError

    async def decrypt(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the plain text of byte-sequence `blob`."""
        raise NotImplementedError

    async def sign(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the digest of byte-sequence `blob`."""
        raise NotImplementedError

    async def verify(self, digest: bytes, blob: bytes,
        *args, **kwargs) -> bytes:
        """Verifies that `digest` is valid for `blob`."""
        raise NotImplementedError
