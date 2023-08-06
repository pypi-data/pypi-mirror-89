"""Declares :class:`JOSESignature`."""
from .utils import base64url_decode


class JOSESignature:
    """Represents the signature on a JSON Web Signature (JWS)."""

    @classmethod
    def parse(cls, buf: bytes, algorithm: str): # pragma: no cover
        return cls(base64url_decode(buf), algorithm)

    def __init__(self, digest, algorithm):
        self.digest = digest
        self.algorithm = algorithm

    async def verify(self, key, data: bytes) -> bool:
        """Verifies the :class:`Signature` for byte-sequence `data` using
        the given key `key`.
        """
        return await key.verify(self.digest, data, algorithm=self.algorithm)

    def __bytes__(self):
        return self.digest
