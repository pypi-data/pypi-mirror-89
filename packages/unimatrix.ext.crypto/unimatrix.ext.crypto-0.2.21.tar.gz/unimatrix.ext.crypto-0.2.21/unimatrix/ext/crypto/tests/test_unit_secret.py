# pylint: skip-file
import asyncio
import unittest

from ..secret import SecretKey


class SecretKeyTestCase(unittest.TestCase):

    def test_sign_and_verify(self):
        k = SecretKey('foo')
        digest = asyncio.run(k.sign(b'bar'))
        self.assertTrue(asyncio.run(k.verify(digest, b'bar')))
