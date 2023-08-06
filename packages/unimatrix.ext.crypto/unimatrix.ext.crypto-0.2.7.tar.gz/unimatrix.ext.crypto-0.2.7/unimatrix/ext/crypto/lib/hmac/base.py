"""Declares :class:`BaseHmacSigner`."""
import hashlib
import hmac

from ...signature import Signature
from ...signer import Signer


class BaseHmacSigner(Signer):
    """Provides the base class for all Hash-Based Message Authentication
    Code (HMAC) signer implementations.
    """
    algorithm = None

    def sign(self, buf):
        return Signature(hmac.new(self.secret, buf, self.hash_func).digest(),
            self.algorithm)


class HMACSHA256Signer(BaseHmacSigner):
    """Create HMAC signatures using SHA-256 as the hashing algorithm."""
    hash_func = hashlib.sha256
    algorithm = 'HS256'
