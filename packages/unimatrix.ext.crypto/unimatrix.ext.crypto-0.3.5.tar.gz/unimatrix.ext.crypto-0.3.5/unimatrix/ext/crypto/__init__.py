"""The :mod:`unimatrix.ext.crypto` package provides an interface to encrypt,
decrypt, sign and verify using various cryptographic backends.


Integration with Django
=======================
The :mod:`unimatrix.ext.crypto` package is a Django application. It is
installed by adding ``unimatrix.ext.crypto`` to the Django ``INSTALLED_APPS``
setting.

The application recognizes the following settings:

- ``CRYPTO_BACKENDS` - The dictionary of cryptographic backends that are
  configured for the Django application. The keys are strings specifying the
  internal names; the values mappings of configuration options. Structure is
  documented below.

The ``CRYPTO_BACKENDS`` setting members support:

- ``backend`` - (Required) The qualified name of the Python package providing
  a cryptographic backend. Valid options are ``unimatrix.ext.crypto.lib.null``,
  ``unimatrix.ext.crypto.lib.google``, ``unimatrix.ext.crypto.lib.aes``.
- ``options`` - (Required) The options to initialize the cryptographic backend
  with. The required keys depend on the backend.


Configuration examples
----------------------
The sections below describe the various Django configurations for specific
cryptographic backends.

Google Cloud KMS
++++++++++++++++

.. code:: python

    INSTALLED_APPS = [
        "unimatrix.ext.crypto",
        # ... other apps
    ]

    CRYPTO_BACKENDS = {
        'default': {
            'backend': "unimatrix.ext.crypto.lib.google",
            'options': {
                'cloud.google.com/project': "myproject",
                'cloudkms.googleapis.com/location': "europe-west4",
                'cloudkms.googleapis.com/keyring': "mykeyring",
                'cloudkms.googleapis.com/key': "mykey",

                # This option is only required for signing backends.
                'cloudkms.googleapis.com/version': 1
            }
        }
    }
"""
from . import algorithms
from .abstractkeystore import AbstractKeystore
from .ciphertext import Ciphertext
from .secret import get_secret_key
from .secret import get_signer
from .secret import SecretKey
from .signable import Signable
from .signature import Signature
from .signer import Signer
from .plaintext import Plaintext
from .private import PrivateKey
from .public import PublicKey


__all__ = [
    'algorithms',
    'backends',
    'get_secret_key',
    'get_signer',
    'SecretKey',
    'Signable',
    'Signature',
    'Signer',
    'PrivateKey',
    'PublicKey',
]
default_app_config = 'unimatrix.ext.crypto.apps.ApplicationConfig'


def plain(pt: bytes, **kwargs) -> Plaintext:
    """Return a :class:`Plaintext` instance configured with the given
    attributes. This function is used for cryptographic algorithms that
    require additional input besided the plaintext itself.

    Args:
        pt: the plain text. If `pt` is :class:`str`, then UTF-8 encoding is
            assumed.

    Returns:
        :class:`Plaintext`

    Below is an example with Authenticated Encryption with Associated Data
    (AEAD):

    .. code:: python

        from unimatrix.ext import crypto

        pt = crypto.plain(b"My secret text", aad=b"Authenticated data")
        print(pt.aad)
    """
    pt = Plaintext(pt)
    for k in dict.keys(kwargs):
        if str.startswith(k, '_'):
            continue
        setattr(pt, k, kwargs[k])
    return pt


AbstractKeyStore = AbstractKeystore
