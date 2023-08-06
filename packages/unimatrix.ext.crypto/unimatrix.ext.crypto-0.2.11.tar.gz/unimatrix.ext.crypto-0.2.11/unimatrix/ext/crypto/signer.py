"""Declares :class:`Signer`."""
import abc

from .oid import HMACSHA256
from .oid import HMACSHA384
from .oid import HMACSHA512
from .signature import Signature


class Signer(metaclass=abc.ABCMeta):
    """Declares the mandatory interface for all :class:`Signer`
    implementations.
    """
    signature_class = Signature

    @abc.abstractmethod
    def sign(self, buf, algorithm=None) -> Signature:
        """Signs byte-sequence `buf` and returns a byte-sequence holding the
        signature.

        Args:
            buf (bytes): the data to be signed.
            algorithm: an instruction for the signer on the algorithm to use.

        Returns:
            :class:`~unimatrix.ext.crypto.Signature`
        """
        raise NotImplementedError

    @abc.abstractproperty
    def algorithm(self) -> str:
        """Returns a string holding an OID, identifying the algorithm
        that the signer uses.
        """
        raise NotImplementedError

    @property
    def public(self):
        """Returns a :class:`unimatrix.ext.crypto.PublicKey` implementation
        that can verify the signatures produced by this signer.
        """
        raise NotImplementedError


class ApplicationSigner(Signer):
    """A :class:`Signer` implementation that is configured with the
    :term:`Application Secret Key`.
    """
    _symbolic_mapping = {
        'sha256': HMACSHA256,
        'sha384': HMACSHA384,
        'sha512': HMACSHA512,
    }

    @property
    def algorithm(self) -> str:
        """Return the algorithm used by the signer."""
        alg = self.key.default_algorithm
        if alg in self._symbolic_mapping:
            alg = self._symbolic_mapping[alg]
        return alg

    def __init__(self, key):
        self.key = key

    def sign(self, buf, algorithm=None) -> Signature:
        """Signs byte-sequence `buf` and returns the corresponding signature.

        Args:
            buf (bytes): the data to be signed.
            algorithm: an instruction for the signer on the algorithm to use.

        Returns:
            :class:`~unimatrix.ext.crypto.Signature`
        """
        return Signature(self.key.sign(buf), self.algorithm)
