"""Declares :class:`JOSEHeader`."""
import base64
import json

from ...oid import OID_JOSE_ALGORITHMS
from .jwt import JSONWebToken
from .utils import base64url_decode
from .utils import base64url_encode
from .utils import json_encode


PROTECTED_PARAMETERS = ["alg", "jku", "jwk", "kid", "x5u", "x5c", "x5t",
    "5t#S256", "typ", "cty", "crit"]


class JOSEHeader:
    """Wraps the header of a JSON Web Signature and Encryption (JOSE)
    object.
    """

    @property
    def algorithm(self):
        """Return the OID identifying the algorithm used with the JOSE
        object.
        """
        print(self.params)
        return OID_JOSE_ALGORITHMS[ self['alg'] ]

    @classmethod
    def parse(cls, encoded):
        return cls(json.loads(base64url_decode(encoded)))

    def __init__(self, params=None):
        self.params = params or {}

    def get_payload(self, payload):
        """Return the approprate instance for the payload."""
        return JSONWebToken.parse(payload)\
            if self.is_jwt() else payload

    def is_jwt(self):
        """Return a boolean indicating if the header was part of a JSON
        Web Token (JWT).
        """
        return self.params.get('typ') == 'JWT'

    def setdefault(self, key, value):
        return self.params.setdefault(key, value)

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, key):
        return self.params[key]

    def __bytes__(self):
        return base64url_encode(json_encode(self.params))
