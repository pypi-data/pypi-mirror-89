"""Declares various utility functions."""
import hashlib

from cryptography.hazmat.primitives import serialization


def get_subject_key_identifier(key):
    """Generate the Subject Key Identifier (SKI) from a public key.

    Args:
        key (:class:`bytes`): the public key, either DER, PEM or OpenSSH
            encoded.

    Returns:
        :class:`str`
    """
    # Check if the key was encoded in the OpenSSH format, and convert it to
    # PEM if so. TODO: This does not support signed SSH keys.
    f = serialization.load_der_public_key
    header = bytes.splitlines(key)[0]
    if bytes.startswith(key, b'ssh'):
        f = serialization.load_ssh_public_key
    elif bytes.startswith(header, b'-----BEGIN'):
        f = serialization.load_pem_public_key

    pub = f(key).public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return hashlib.sha256(pub).hexdigest()
