"""Declares :class:`JSONWebToken`."""
import json
import time

from . import exceptions
from .utils import base64url_decode
from .utils import base64url_encode
from .utils import json_encode


class JSONWebToken:
    """Represents a JSON Web Token (JWT).

    Args:
        claims (:class:`dict`): the dictionary holding the claims specified
            for the token.
    """
    Expired = exceptions.Expired
    InvalidAudience = exceptions.InvalidAudience
    MalformedToken = exceptions.MalformedToken

    @property
    def aud(self) -> set:
        """Return the value of the `aud` claim."""
        aud = self.claims.get('aud') or []
        if aud is not None and not isinstance(aud, list):
            if not isinstance(aud, str):
                raise self.MalformedToken
            aud = [aud]
        return set(aud)

    @property
    def exp(self) -> int:
        """Return the expiry date/time, in seconds since the UNIX epoch,
        as specified by the `exp` claim.
        """
        if not self.claims.get('exp'):
            return None

        try:
            return int(self.claims['exp'])
        except ValueError:
            raise self.MalformedToken

    @property
    def iss(self) -> str:
        """Return the issues as specified by the `iss` claim."""
        return self.claims.get('iss')

    @classmethod
    def parse(cls, value):
        return cls(json.loads(base64url_decode(value)))

    def __init__(self, claims: dict):
        self.claims = claims

    def verify_audience(self, audiences, raise_exception=True):
        """Verifies that the `aud` claim matches one or more of the specified
        `audiences`.
        """
        if isinstance(audiences, str):
            audiences = [audiences]
        audiences = set(audiences)

        is_valid = bool(self.aud & audiences)
        if not is_valid and raise_exception:
            raise self.InvalidAudience(self, audiences)
        return is_valid

    def verify_expired(self, now=None, raise_exception=True):
        """Verifies that the JSON Web Token is not expired, based on the
        `exp` claim.
        """
        if self.exp is None:
            return True

        if now is None:
            now = int(time.time())
        is_valid = self.exp >= now
        if not is_valid and raise_exception:
            raise self.Expired(self, now)
        return is_valid

    def __bytes__(self):
        return base64url_encode(json_encode(self.claims))
