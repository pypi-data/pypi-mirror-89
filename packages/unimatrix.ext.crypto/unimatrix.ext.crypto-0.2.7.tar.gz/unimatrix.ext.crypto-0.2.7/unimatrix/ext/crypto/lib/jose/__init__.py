# pylint: skip-file
from .header import JOSEHeader
from .jws import JSONWebSignature
from .jwt import JSONWebToken


__all__ = [
    'JSONWebSignature'
]


def parse_jose_object(value):
    """Parse a JOSE object from the given value. Inspect the JOSE header and
    return the appropriate object.
    """
    header, *parts = bytes.split(b'.', value)
    if len(parts) != 2:
        raise NotImplementedError

    return JSONWebSignature.parse(value)
