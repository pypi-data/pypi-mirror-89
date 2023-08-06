"""Implements the Public-Key Cryptography Standards (PKCS)."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from . import oid
from .private import PrivateKey


class RSAPrivateKey(PrivateKey):
    """Uses an RSA private key to perform cryptographic operations.
    
    The options format recognized by this implementation is specified below:

    .. code:: python

        {
            "path": "/path/to/private/key"
        }
    """
    capabilities = [
        oid.RSAPKCS1v15SHA256,
        oid.RSAPKCS1v15SHA384,
        oid.RSAPKCS1v15SHA512,
        oid.RSAOAEP
    ]

    def setup(self, opts):
        """Configures the :class:`RSAPrivateKey` using the given options `opts`.
        This method is called in the constructor and should not be called more
        than once.
        """
        self._private = load_pem_private_key(
            open(opts.path, 'rb').read(), opts.get('password'))
        self._public = self._private.public_key()

    async def decrypt(self, ct, padding):
        return self._private.decrypt(bytes(ct), padding)

    async def encrypt(self, pt, padding):
        return self._public.encrypt(bytes(pt), padding)

    async def sign(self, blob: bytes, padding, algorithm) -> bytes:
        return self._private.sign(blob, padding, algorithm)

    async def verify(self, digest: bytes, blob: bytes,
        padding, algorithm) -> bytes:
        try:
            self._public.verify(bytes(digest), blob, padding, algorithm)
            return True
        except InvalidSignature:
            return False
