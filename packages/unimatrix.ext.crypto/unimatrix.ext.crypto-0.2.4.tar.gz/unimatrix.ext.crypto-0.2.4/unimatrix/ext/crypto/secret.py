"""Declares :class:`SecretKey`."""
import hashlib
import hmac

from unimatrix.conf import settings

from .lib.aes import AESPrivateKey
from .oid import HMACSHA256
from .oid import HMACSHA384
from .oid import HMACSHA512

class SecretKey:
    """A :class:`~unimatrix.ext.crypto.PrivateKey` implementation that is
    commonly used as a secret for an application. It supports signing/verifying
    using HMAC, and encryption with AES.

    Args:
        secret: a byte-sequence or string holding the secret.
    """
    _algorithms = {
        HMACSHA256: hashlib.sha256,
        HMACSHA384: hashlib.sha384,
        HMACSHA512: hashlib.sha512,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512
    }

    @classmethod
    def default(cls, algorithm=None):
        """Return the default secret key as specified by the settings."""
        return cls(settings.SECRET_KEY,
            getattr(settings, 'DEFAULT_HMAC_ALGORITHM', algorithm))

    def __init__(self, secret, default_algorithm='sha256'):
        if isinstance(secret, str):
            secret = str.encode(secret, 'ascii')
        self.secret = secret
        self.aes = AESPrivateKey(hashlib.sha256(self.secret).digest())
        self.default_algorithm = default_algorithm or 'sha256'

    def _hashfunc(self, algorithm):
        return self._algorithms[algorithm or self.default_algorithm]

    def sign(self, buf, algorithm=None):
        """Sign byte-sequence `buf` with the given algorithm."""
        return hmac.new(self.secret, buf, self._hashfunc(algorithm)).digest()

    def verify(self, signature, buf, algorithm=None):
        """Verify that byte-sequence `signature` was created from
        byte-sequence `buf` using the given `algorithm`.
        """
        return hmac.compare_digest(signature, self.sign(buf, algorithm))
