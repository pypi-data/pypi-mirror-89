# pylint: skip-file
import unittest

from .... import oid
from ....signer import Signer
from ....secret import SecretKey
from ..header import JOSEHeader
from ..jws import JSONWebSignature
from ..jwt import JSONWebToken


class HMACSigner(Signer):
    algorithm = None

    def __init__(self, alg):
        self.algorithm = alg
        self.key = SecretKey('foo', alg)

    def sign(self, buf, *args, **kwargs):
        return self.signature_class(self.key.sign(buf, self.algorithm),
            self.algorithm)


class JSONWebSignatureTestCase(unittest.TestCase):

    def setUp(self):
        self.header = JOSEHeader()
        self.jws = JSONWebSignature(self.header, JSONWebToken({'iss': "queen"}))

    def test_header_sets_correct_type(self):
        self.assertEqual(self.jws.header.params['typ'], 'JWT')

    def test_sign_and_parse(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = self.jws.sign(signer)
        jws = JSONWebSignature.parse(bytes(self.jws))

        self.assertEqual(jws.payload.iss, self.jws.payload.iss)

    def test_sign_symmetric_hmacsha256(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = self.jws.sign(signer)
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(self.jws.verify(signer.key))
        self.assertFalse(sig.verify(signer.key, b'foo'))

    def test_sign_symmetric_hmacsha384(self):
        signer = HMACSigner(oid.HMACSHA384)
        sig = self.jws.sign(signer)
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(self.jws.verify(signer.key))
        self.assertFalse(sig.verify(signer.key, b'foo'))

    def test_sign_symmetric_hmacsha512(self):
        signer = HMACSigner(oid.HMACSHA512)
        sig = self.jws.sign(signer)
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(self.jws.verify(signer.key))
        self.assertFalse(sig.verify(signer.key, b'foo'))
