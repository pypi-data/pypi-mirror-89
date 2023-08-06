"""Declares :class:`JSONWebToken`."""
from .utils import base64url_encode
from .utils import json_encode


class JSONWebToken:
    """Represents a JSON Web Token (JWT).

    Args:
        claims (:class:`dict`): the dictionary holding the claims specified
            for the token.
    """

    def __init__(self, claims: dict):
        self.claims = claims

    def __bytes__(self):
        return base64url_encode(json_encode(self.claims))
