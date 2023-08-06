"""Specifies the algorithms available to the :mod:`unimatrix.ext.crypto`
package.

Encryption algorithms
+++++++++++++++++++++

.. py:attribute:: RSAOAEPSHA256

    RSA with Optimal Asymmetric Encryption Padding (OAEP) and hash
    algorithm SHA-256.

Signing algorithms
++++++++++++++++++

.. py:attribute:: RSAPKCS1v15SHA256

    RSA with PKCS#1 version 1.5 padding and hash algorithm SHA-256.

.. py:attribute:: RSAPKCS1v15SHA384

    RSA with PKCS#1 version 1.5 padding and hash algorithm SHA-384.

.. py:attribute:: RSAPKCS1v15SHA512

    RSA with PKCS#1 version 1.5 padding and hash algorithm SHA-512.
"""
from .rsa import *
