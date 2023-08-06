"""Declares :class:`JSONWebSignature`."""
import base64
import json
from typing import Any

from ...oid import OID_JOSE_ALGORITHMS
from ...signer import Signer
from ...signable import Signable
from .header import JOSEHeader
from .signature import JOSESignature
from .utils import base64url_decode
from .utils import base64url_encode


class JSONWebSignature(Signable):
    """Represents a JSON Web Signature (JWS) as specified in :rfc:`7515`.

    Args:
        payload: the payload of the JSON Web Signature.
    """
    payload: Any

    @classmethod
    def parse(cls, token):
        """Parse a :class:`JSONWebSignature` from a byte-sequence or string."""
        if isinstance(token, str):
            token = str.encode(token)
        header, payload, signature = bytes.split(token, b'.')
        header = JOSEHeader.parse(header)
        return cls(
            header,
            header.get_payload(payload),
            JOSESignature(base64url_decode(signature), header.algorithm)
        )

    def __init__(self, header, payload, signature=None):
        self.header = header
        self.header.setdefault('typ', 'JWS')
        self.payload = payload
        self.signature = signature

    def get_jose_header(self, signer: Signer):
        """Return a :class:`~unimatrix.ext.crypto.lib.jose.JOSEHeader` instance
        based on the metadata of :class:`~unimatrix.ext.crypto.signer.Signer`
        `signer`.
        """
        self.header['alg'] = OID_JOSE_ALGORITHMS[signer.algorithm]
        return bytes(self.header)

    def get_signable_bytes(self, signer: Signer):
        """Return a byte-sequence holding the data that needs to be signed
        for the :class:`JSONWebSignature`.
        """
        return self.get_jose_header(signer) + b'.' + bytes(self.payload)

    def verify(self, key):
        """Verify the :class:`JSONWebSignature` with the given key."""
        return self.signature.verify(key, bytes.join(b'.', [
            bytes(self.header),
            bytes(self.payload)
        ]))

    def __str__(self):
        return str.join('.', [
            bytes.decode(bytes(self.header)),
            bytes.decode(bytes(self.payload)),
            bytes.decode(base64url_encode(bytes(self.signature)))
        ])
