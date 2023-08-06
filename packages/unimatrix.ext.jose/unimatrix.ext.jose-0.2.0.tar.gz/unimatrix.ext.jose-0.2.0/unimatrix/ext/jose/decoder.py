"""Declares :class:`JOSEPayloadDecoder`."""


class JOSEPayloadDecoder:
    """Provides an interface to get the payload of a JSON Web Signature (JWS)
    or JSON Web Encryption (JWE).
    """

    async def get_payload(self, obj):
        pass

    @ioc.inject.context('keystore', 'Keystore')
    async def verify(self, jws):
        """Verifies the integrity of a JSON Web Signature (JWS)."""
        key = await keystore.get(jws.header.kid)
        return await jws.verify(key)
