"""Declares :class:`JOSEHeader`."""
import json

from ...oid import OID_JOSE_ALGORITHMS
from ...oid import OID_JOSE_JWE_ENC
from ...oid import OID_JOSE_JWE_ALG
from ...oid import OID_JOSE_JWS_ALG
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
        return OID_JOSE_ALGORITHMS[ self['alg'] ]

    @classmethod
    def parse(cls, encoded):
        params = json.loads(base64url_decode(encoded))

        # Check if the required `alg` parameter specifies a supported
        # algorithm.
        if params['alg'] not in OID_JOSE_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {params['alg']}")

        # If the `enc` parameter is present, the input is JSON Web
        # Encryption (JWE) and must be supported. When the `enc` parameter
        # is not present, we're dealing with a JWS.
        if params.get('enc'):
            if params.get('alg') not in  OID_JOSE_JWE_ALG:
                raise ValueError(f"Unsupported algorithm: {alg}")
            if params['enc'] not in OID_JOSE_JWE_ENC:
                raise ValueError(
                    f"Unsupported encryption algorithm: {params['enc']}")
        elif params.get('alg') not in  OID_JOSE_JWS_ALG:
            raise ValueError(f"Unsupported algorithm: {params['alg']}")

        return cls(params)

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
        return str.lower(self.params.get('typ') or '') == 'jwt'

    def setdefault(self, key, value):
        return self.params.setdefault(key, value)

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, key):
        return self.params[key]

    def __bytes__(self):
        return base64url_encode(json_encode(self.params))
