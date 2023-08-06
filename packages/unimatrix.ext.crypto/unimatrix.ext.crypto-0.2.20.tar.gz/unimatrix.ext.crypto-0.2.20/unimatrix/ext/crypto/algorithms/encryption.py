"""Declares :class:`EncryptionAlgorithm`."""
import abc

from ..ciphertext import CipherText


class EncryptionAlgorithm(metaclass=abc.ABCMeta):
    ct_class = CipherText

    async def encrypt(self, key, pt: bytes) -> bytes:
        if not await key.can_use(self.oid):
            raise IncompatibleKey
        ct = await key.encrypt(pt, **self.get_encrypt_parameters(key))
        return self.ct_class(ct, self)

    async def decrypt(self, key, ct: bytes):
        if not await key.can_use(self.oid):
            raise IncompatibleKey
        return await key.decrypt(ct, **self.get_decrypt_parameters(key, ct))

    @abc.abstractmethod
    def get_encrypt_parameters(self, key) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_decrypt_parameters(self, key, ct) -> dict:
        raise NotImplementedError
