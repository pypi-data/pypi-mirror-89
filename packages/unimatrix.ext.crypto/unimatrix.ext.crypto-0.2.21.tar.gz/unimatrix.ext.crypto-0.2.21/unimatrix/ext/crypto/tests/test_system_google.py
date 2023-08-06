# pylint: skip-file
import asyncio
import os
import unittest

from ..algorithms import RSAPKCS1v15SHA256
from ..algorithms import RSAOAEPSHA256
from ..defaultkeystore import DefaultKeystore
from ..google import GoogleManagedKey
from .base import EncryptionTestCase
from .base import SigningTestCase
from .base import async_test


ks = DefaultKeystore({
    'google_sign': {
        'class': "unimatrix.ext.crypto.google.GoogleManagedKey",
        'keyid': "dbdbc0427ec5f0c3f667c7bacff574c9",
        'options': {
            'project': "unimatrixtesting",
            'location': "europe-west4",
            'keyring': "default",
            'key': "rsa_sign_pkcs1_4096_sha256",
            'version': 3
        }
    },
    'google_encrypt': {
        'class': "unimatrix.ext.crypto.google.GoogleManagedKey",
        'keyid': "867546f4b1bb775bc0c649bae98d10cb",
        'options': {
            'project': "unimatrixtesting",
            'location': "europe-west4",
            'keyring': "default",
            'key': "rsa_decrypt_oaep_4096_sha256",
            'version': 1
        }
    },
})


@unittest.skipIf(not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    "GOOGLE_APPLICATION_CREDENTIALS is not supplied.")
class RSAPKCS1v15SHA256TestCase(SigningTestCase):
    __test__ = True
    algorithm = RSAPKCS1v15SHA256

    @async_test
    async def get_private_key(self):
        return await ks.get('google_sign')


@unittest.skipIf(not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    "GOOGLE_APPLICATION_CREDENTIALS is not supplied.")
class RSAOAEPSHA256TestCase(EncryptionTestCase):
    __test__ = True
    algorithm = RSAOAEPSHA256

    @async_test
    async def get_private_key(self):
        return await ks.get('google_encrypt')
