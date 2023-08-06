"""Declares :class:`SecretKey`."""
import hashlib
import hmac

from unimatrix.conf import settings

from . import oid
from .ciphertext import Ciphertext
from .plaintext import Plaintext
from .private import PrivateKey
from .signer import ApplicationSigner


class SecretKey(PrivateKey):
    """A :class:`~unimatrix.ext.crypto.PrivateKey` implementation that is
    commonly used as a secret for an application. It supports signing/verifying
    using HMAC, and encryption with AES.
    """
    capabilities = [
        oid.HMACSHA224,
        oid.HMACSHA256,
        oid.HMACSHA384,
        oid.HMACSHA512,
        oid.AES256GCM
    ]

    _algorithms = {
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
    }

    @classmethod
    def default(cls, algorithm=None):
        """Return the default secret key as specified by the settings."""
        return cls({'secret': settings.SECRET_KEY})

    def setup(self, opts):
        self._secret = str.encode(opts.secret)\
            if isinstance(opts.secret, str)\
            else opts.secret

    def _hashfunc(self, algorithm):
        return self._algorithms[algorithm]

    async def decrypt(self, ct: Ciphertext, apply_decrypt) -> bytes:
        return await apply_decrypt(self._secret, ct)

    async def encrypt(self, pt: Plaintext, apply_encrypt, **kwargs) -> bytes:
        return await apply_encrypt(self._secret, pt, **kwargs)

    async def sign(self, blob: bytes, algorithm: str) -> bytes:
        """Sign byte-sequence `blob` with the given algorithm."""
        return hmac.new(self._secret, blob, self._hashfunc(algorithm)).digest()

    async def verify(self, digest: bytes, blob: bytes, algorithm: str) -> bytes:
        """Verify that byte-sequence `digest` was created from
        byte-sequence `blob` using the given `algorithm`.
        """
        return hmac.compare_digest(digest, await self.sign(blob, algorithm))


def get_secret_key():
    """Return the default secret key used by an application, as configured
    in :mod:`unimatrix.conf`. The underlying settings module (specified by
    :envvar:`UNIMATRIX_SETTINGS_MODULE`) must expose a ``SECRET_KEY`` attribute
    that holds the private key.
    """
    return SecretKey.default()


def get_signer():
    """Return a :class:`~unimatrix.ext.crypto.Signer` implementation
    configured with the default secret key (as returned by
    :func:`get_secret_key()`) and algorithm.
    """
    return ApplicationSigner(get_secret_key())
