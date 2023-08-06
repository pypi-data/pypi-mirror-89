"""Declares :class:`PrivateKey`."""
import abc


class PrivateKey(metaclass=abc.ABCMeta):
    """Provides an interface for signing and decryption
    operations.
    """

    @abc.abstractmethod
    async def encrypt(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the cipher text of byte-sequence `blob`."""
        raise NotImplementedError

    @abc.abstractmethod
    async def decrypt(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the plain text of byte-sequence `blob`."""
        raise NotImplementedError

    @abc.abstractmethod
    async def sign(self, blob: bytes, *args, **kwargs) -> bytes:
        """Returns the digest of byte-sequence `blob`."""
        raise NotImplementedError

    @abc.abstractmethod
    async def verify(self, digest: bytes, blob: bytes,
        *args, **kwargs) -> bytes:
        """Verifies that `digest` is valid for `blob`."""
        raise NotImplementedError
