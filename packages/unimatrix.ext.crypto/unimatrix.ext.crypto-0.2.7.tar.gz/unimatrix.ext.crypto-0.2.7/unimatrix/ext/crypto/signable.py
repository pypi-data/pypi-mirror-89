"""Declares :class:`Signable`."""
import abc

from .signer import Signer
from .signature import Signature


class Signable(metaclass=abc.ABCMeta):
    """Specifies the basic interface for signable objects."""
    signature: Signature = None

    @abc.abstractmethod
    def get_signable_bytes(self, signer: Signer) -> bytes:
        """Return a byte-sequence holding the data that needs to be signed
        for the :class:`Signable`.
        """
        raise NotImplementedError

    def sign(self, signer: Signer):
        """Use `signer` to create a signature."""
        if self.signature is None:
            self.signature = signer.sign(self.get_signable_bytes(signer))
        return self.signature
