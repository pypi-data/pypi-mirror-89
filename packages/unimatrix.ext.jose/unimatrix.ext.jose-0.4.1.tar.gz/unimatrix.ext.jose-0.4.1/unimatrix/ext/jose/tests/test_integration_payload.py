# pylint: skip-file
import unittest
from unittest.mock import AsyncMock

import ioc

from unimatrix.ext import jose
from ..decoder import JOSEPayloadDecoder
from ..resolver import JOSEKeyResolver
from .signer import HMACSigner


class PayloadDecodingTestCase(unittest.TestCase):

    def setUp(self):
        self.signer = HMACSigner()
        self.jws = jose.jwt.sync({'sub': 'Foo Bar'}, signer=self.signer)
        ioc.provide('JOSEPayloadDecoder', JOSEPayloadDecoder())
        ioc.provide('JOSEKeyResolver', JOSEKeyResolver())
        ioc.provide('CryptoKeyStore', AsyncMock())

    def test_decode_jws_payload(self):
        self.assertTrue(self.jws.is_signed())
        jwt = jose.payload.sync(bytes(self.jws))
