"""Declares :class:`Signature`."""
import abc

from .const import OID_MAPPING


class Signature(metaclass=abc.ABCMeta):
    """Provides the interface for digital signatures."""
    __module__ = 'unimatrix.ext.crypto'
    InvalidSignature = type('InvalidSignature', (Exception,), {})

    def __init__(self, buf, algorithm):
        self.__data = buf
        self.__algorithm = algorithm
        self.__padding, self.__hashing = None, None
        if self.__algorithm in OID_MAPPING:
            self.__padding, self.__hashing = OID_MAPPING[algorithm]

    def to_bytes(self):
        """Return a binary representation of the signature."""
        return self.__data

    async def verify(self, key, data: bytes, suppress=False) -> bool:
        """Verifies the :class:`Signature` using the given public key
        `key`.
        """
        is_valid = await self.__algorithm.verify(key, self.__data, data)
        if not is_valid and not suppress:
            raise self.InvalidSignature
        return is_valid

    def __bytes__(self):
        return self.to_bytes()
