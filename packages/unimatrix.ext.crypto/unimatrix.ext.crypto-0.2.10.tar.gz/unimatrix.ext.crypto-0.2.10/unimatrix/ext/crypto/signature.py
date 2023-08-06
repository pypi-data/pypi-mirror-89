"""Declares :class:`Signature`."""
import abc

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

from .const import OID_MAPPING


class Signature(metaclass=abc.ABCMeta):
    """Provides the interface for digital signatures."""

    def __init__(self, buf, algorithm):
        self.__data = buf
        self.__algorithm = algorithm
        self.__padding, self.__hashing = None, None
        if self.__algorithm in OID_MAPPING:
            self.__padding, self.__hashing = OID_MAPPING[algorithm]

    def to_bytes(self):
        """Return a binary representation of the signature."""
        return self.__data

    def verify(self, key, data, prehashed=False):
        """Verifies the :class:`Signature` using the given public key
        `key`.
        """
        if not self.__padding:
            return key.verify(bytes(self), data)

        try:
            key.verify(bytes(self), data, self.__padding,
                self.__hashing if not prehashed else Prehashed(self.__hashing))
            return True
        except InvalidSignature:
            return False

    def __bytes__(self):
        return self.to_bytes()
