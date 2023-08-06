"""Declares :class:`JOSESignature`."""
from unimatrix.ext import crypto

from .utils import base64url_decode


class JOSESignature(crypto.Signature):
    """Represents the signature on a JSON Web Signature (JWS)."""
    pass
