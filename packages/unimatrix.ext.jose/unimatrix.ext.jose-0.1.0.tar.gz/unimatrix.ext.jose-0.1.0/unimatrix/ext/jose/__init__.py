# pylint: skip-file
from unimatrix.lib import meta

from .exceptions import BaseJoseException
from .exceptions import MalformedToken
from .header import JOSEHeader
from .jws import JSONWebSignature
from .jwt import JSONWebToken


__all__ = [
    'JSONWebSignature',
    'JSONWebToken',
    'JWT',
    'parse_jose_object',
]


def parse(value):
    """Parse a JOSE object from the given value. Inspect the JOSE header and
    return the appropriate object.

    Args:
        value: a :class:`str` or :class:`bytes` object holding the compact
            representation of the JOSE object.

    Raises:
        :exc:`MalformedToken`: `value` is not a compact representation of a
            JOSE object.
        :exc:`UnsupportedAlgorithm`: the JOSE header is valid but the
            signing or wrapping algorithm (specified by the ``alg`` header 
            parameter) is not recognized.
        :exc:`UnsupportedEncryptionAlgorithm`: the JOSE header is valid but
            the encryption algorithm (specified by the ``enc`` header parameter)
            is not recognized.

    Returns:
        :class:`JSONWebSignature`,
        :class:`JSONEncryption`

    The :func:`parse()` function selects the appropriate type by inspecting the
    header, which results in returning either a :class:`JSONWebSignature` or a
    :class:`JSONWebEncryption` instance. In neither case is the JOSE object
    verified or decrypted - it is up to the caller to decided when and in
    what order to process it.
    """
    header, *parts = bytes.split(value, b'.')
    if len(parts) != 2:
        raise MalformedToken
    return JSONWebSignature.parse(value)



@meta.allow_sync
async def JWT(claims: dict, header: dict = None, signer = None):
    """Create a new :class:`JSONWebSignature` holding a signed set of claims
    represented as a :class:`JSONWebToken`. Use `signer` to create a digital
    signature.

    If `signer` is ``None``, the return value is **not** signed, and the caller
    must invoke :meth:`JSONWebSignature.sign()` prior to serializing the
    resulting object.

    >>> from unimatrix.ext import jose
    >>>
    >>> jwt = jose.JWT({'sub': "iamhere"})
    >>> assert jwt.sub == 'iamhere'
    """
    jws = JSONWebSignature(
        JOSEHeader(header or {}),
        JSONWebToken(claims)
    )
    if signer is not None:
        await jws.sign(signer)
    return jws
