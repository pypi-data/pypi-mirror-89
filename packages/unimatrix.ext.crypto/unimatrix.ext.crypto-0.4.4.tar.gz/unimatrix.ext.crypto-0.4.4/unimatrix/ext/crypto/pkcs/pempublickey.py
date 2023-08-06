"""Declares :class:`PEMPublicKey`."""
from .pkcspublic import PKCSPublic


class PEMPublicKey(PKCSPublic):

    def __init__(self, key):
        self._public = key
