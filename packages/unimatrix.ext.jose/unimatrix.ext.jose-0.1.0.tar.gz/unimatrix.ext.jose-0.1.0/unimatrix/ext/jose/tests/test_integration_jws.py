# pylint: skip-file
import asyncio
import unittest

from unimatrix.ext import crypto
from unimatrix.ext.crypto import oid
from .. import JWT
from ..header import JOSEHeader
from ..jws import JSONWebSignature
from ..jwt import JSONWebToken
from ..signature import JOSESignature


class HMACSigner(crypto.Signer):
    algorithm = None
    signature_class = JOSESignature

    def __init__(self, alg):
        self.algorithm = alg
        self.key = crypto.SecretKey('foo', alg)

    async def sign(self, buf, *args, **kwargs):
        return self.signature_class(await self.key.sign(buf, self.algorithm),
            self.algorithm)


class JSONWebSignatureTestCase(unittest.TestCase):

    def setUp(self):
        self.header = JOSEHeader()
        self.jws = JSONWebSignature(self.header, JSONWebToken({'iss': "queen"}))

    def test_create_without_signing(self):
        jws = asyncio.run(JWT({'sub': 'foo'}))

    def test_create_with_signing(self):
        jws = asyncio.run(JWT({'sub': 'foo'}, signer=HMACSigner(oid.HMACSHA256)))

    def test_header_sets_correct_type(self):
        self.assertEqual(self.jws.header.params['typ'], 'JWT')

    def test_sign_and_parse_from_string(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = asyncio.run(self.jws.sign(signer))
        jws = JSONWebSignature.parse(str(self.jws))

        self.assertEqual(jws.payload.iss, self.jws.payload.iss)

    def test_sign_and_parse_from_bytes(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = asyncio.run(self.jws.sign(signer))
        jws = JSONWebSignature.parse(bytes(self.jws))

        self.assertEqual(jws.payload.iss, self.jws.payload.iss)

    def test_sign_and_parse(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = asyncio.run(self.jws.sign(signer))
        jws = JSONWebSignature.parse(bytes(self.jws))

        self.assertEqual(jws.payload.iss, self.jws.payload.iss)

    def test_sign_symmetric_hmacsha256(self):
        signer = HMACSigner(oid.HMACSHA256)
        sig = asyncio.run(self.jws.sign(signer))
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(asyncio.run(self.jws.verify(signer.key)))
        self.assertFalse(asyncio.run(sig.verify(signer.key, b'foo')))

    def test_sign_symmetric_hmacsha384(self):
        signer = HMACSigner(oid.HMACSHA384)
        sig = asyncio.run(self.jws.sign(signer))
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(asyncio.run(self.jws.verify(signer.key)))
        self.assertFalse(asyncio.run(sig.verify(signer.key, b'foo')))

    def test_sign_symmetric_hmacsha512(self):
        signer = HMACSigner(oid.HMACSHA512)
        sig = asyncio.run(self.jws.sign(signer))
        self.assertEqual(self.jws.signature, sig)
        self.assertTrue(asyncio.run(self.jws.verify(signer.key)))
        self.assertFalse(asyncio.run(sig.verify(signer.key, b'foo')))
