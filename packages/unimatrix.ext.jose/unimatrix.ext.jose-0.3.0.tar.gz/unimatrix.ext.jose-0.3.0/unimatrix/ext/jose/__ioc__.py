# pylint: skip-file
import ioc

from .resolver import JOSEKeyResolver


def setup_ioc():
    if not ioc.is_satisfied('JOSEKeyResolver'):
        ioc.provide('JOSEKeyResolver', JOSEKeyResolver())
