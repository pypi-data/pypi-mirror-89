# pylint: skip-file
from .exceptions import BaseJoseException
from .exceptions import MalformedToken
from .header import JOSEHeader
from .jws import JSONWebSignature
from .jwt import JSONWebToken


__all__ = [
    'JSONWebSignature',
    'JSONWebToken',
    'parse_jose_object',
]


def parse(value):
    """Parse a JOSE object from the given value. Inspect the JOSE header and
    return the appropriate object.
    """
    header, *parts = bytes.split(value, b'.')
    if len(parts) != 2:
        raise MalformedToken
    return JSONWebSignature.parse(value)
