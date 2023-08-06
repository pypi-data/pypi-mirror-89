"""Declares :class:`GoogleManagedKey`."""
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from google.cloud import kms
from google.cloud.kms import CryptoKeyVersion

from . import oid
from .private import PrivateKey


GoogleAlgorithm = CryptoKeyVersion.CryptoKeyVersionAlgorithm
CRYPTO_KEY_ALGORITHMS_OIDS = {
    GoogleAlgorithm.RSA_SIGN_PKCS1_2048_SHA256: oid.RSAPKCS1v15SHA256,
    GoogleAlgorithm.RSA_SIGN_PKCS1_3072_SHA256: oid.RSAPKCS1v15SHA256,
    GoogleAlgorithm.RSA_SIGN_PKCS1_4096_SHA256: oid.RSAPKCS1v15SHA256,
    GoogleAlgorithm.RSA_SIGN_PKCS1_4096_SHA512: oid.RSAPKCS1v15SHA512,
    GoogleAlgorithm.RSA_DECRYPT_OAEP_2048_SHA256: oid.RSAOAEP,
    GoogleAlgorithm.RSA_DECRYPT_OAEP_3072_SHA256: oid.RSAOAEP,
    GoogleAlgorithm.RSA_DECRYPT_OAEP_4096_SHA256: oid.RSAOAEP,
    GoogleAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION: oid.AES256GCM,
}


class GoogleManagedKey(PrivateKey):
    """A :class:`PrivateKey` implementation that uses Google Key Management
    Service (KMS) for sign, verify, encrypt and decrypt operations.

    :class:`GoogleManagedKey` is configured with the following options:

    .. code:: python

        {
            'project': "myproject",
            'location': "location e.g. europe-west4",
            'keyring': "keyring",
            'key': "key",

            # The version parameter is required for asymmetric
            # signing/encryption keys. It should be omitted for
            # symmetric keys.
            'version': 3
        }


    This class is a wrapper for all key types supported by Google KMS. The
    capabilities will be determined dynamically based on the key metadata.
    """
    capabilities = None

    @property
    def kms(self):
        if not hasattr(self, '_kms'):
            self._kms = kms.KeyManagementServiceAsyncClient()
        return self._kms

    @property
    def resource_id(self):
        if not hasattr(self, '_resource_id'):
            func = self.kms.crypto_key_path
            args = [self.opts.project, self.opts.location, self.opts.keyring,
                self.opts.key]
            if self.opts.get('version'):
                args.append(self.opts.version)
                func = self.kms.crypto_key_version_path
            self._resource_id = func(*args)
        return self._resource_id

    def setup(self, opts):
        self._capabilities = None
        self._public = None

    async def can_use(self, oid):
        if self._capabilities is None:
            k = await self._get_crypto_key()
            self._capabilities = [ CRYPTO_KEY_ALGORITHMS_OIDS[k.algorithm] ]
        return oid in self._capabilities

    async def decrypt(self, ct, *args, **kwargs):
        return await (
            self.decrypt_symmetric(ct)\
            if oid.AES256GCM in self._capabilities\
            else self.decrypt_asymmetric(ct)
        )

    async def decrypt_asymmetric(self, ct):
        response = await self.kms.asymmetric_decrypt({
            'name': self.resource_id,
            'ciphertext': bytes(ct)
        })
        return response.plaintext

    async def decrypt_symmetric(self, ct):
        params = {
            'name': self.resource_id,
            'ciphertext': bytes(ct)
        }
        if hasattr(ct, 'aad'):
            params['additional_authenticated_data'] = ct.aad
        response = await self.kms.decrypt(params)
        return response.plaintext

    async def encrypt(self, pt, *args, **kwargs):
        return await (
            self.encrypt_symmetric(pt)\
            if oid.AES256GCM in self._capabilities\
            else self.encrypt_asymmetric(pt, kwargs['padding'])
        )

    async def encrypt_asymmetric(self, pt, padding):
        if not self._public:
            pub = await self.kms.get_public_key({'name': self.resource_id})
            self._public = load_pem_public_key(str.encode(pub.pem, 'utf-8'))
        return self._public.encrypt(bytes(pt), padding)

    async def encrypt_symmetric(self, pt, *args, **kwargs):
        params = {
            'name': self.resource_id,
            'plaintext': bytes(pt)
        }
        if hasattr(pt, 'aad'):
            params['additional_authenticated_data'] = pt.aad
        response = await self.kms.encrypt(params)
        return response.ciphertext

    async def sign(self, blob: bytes, algorithm, **kwargs) -> bytes:
        h = getattr(hashlib, algorithm.name)(blob)
        response = await self.kms.asymmetric_sign({
            'name': self.resource_id,
            'digest': {algorithm.name: h.digest()}
        })
        return response.signature

    async def verify(self, digest, blob, algorithm, padding, **kwargs) -> bytes:
        if not self._public:
            pub = await self.kms.get_public_key({'name': self.resource_id})
            self._public = load_pem_public_key(str.encode(pub.pem, 'utf-8'))
        try:
            self._public.verify(bytes(digest), blob, padding, algorithm)
            return True
        except InvalidSignature:
            return False

    async def _get_crypto_key(self):
        f = self.kms.get_crypto_key\
            if not self.opts.get('version')\
            else self.kms.get_crypto_key_version
        k = await(f({'name': self.resource_id}))
        return k.primary if not self.opts.get('version') else k
