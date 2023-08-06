"""Declares :class:`PublicKey`."""
import abc


class PublicKey(metaclass=abc.ABCMeta):
    """Declares the interface for public key."""

    @abc.abstractmethod
    async def verify(self, digest: bytes, blob: bytes,
        *args, **kwargs) -> bytes:
        """Verifies that `digest` is a valid signature with this public
        key on `blob`.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def encrypt(self, pt: bytes, *args, **kwargs) -> bytes:
        """Encrypt byte-sequence `pt` using the specified parameters."""
        raise NotImplementedError


def load_pem_public_key(blob):
    """Load byte-sequence `blob` holding a PEM-serialized PKCS#1 DER encoded
    public key as a :class:`PublicKey` instance.
    """
    from .lib.pkcs import PEMPublicKey
    return PEMPublicKey.frompem(blob)
