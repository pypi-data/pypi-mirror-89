"""
**Deal** is a Python library for [design by contract][wiki] (DbC) programming.
See [documentation][docs] for more details.

[wiki]: https://en.wikipedia.org/wiki/Design_by_contract
[docs]: https://deal.readthedocs.io/index.html
"""

# main package info
__title__ = 'deal'
__version__ = '4.5.0'
__author__ = 'Gram Orsinium'
__license__ = 'MIT'


# app
from ._aliases import chain, ensure, has, inv, post, pre, pure, raises, reason, safe
from ._exceptions import *  # noQA
from ._imports import activate, module_load
from ._schemes import Scheme
from ._state import disable, enable, reset
from ._testing import TestCase, cases


__all__ = [
    'cases',
    'Scheme',
    'TestCase',

    # state
    'disable',
    'enable',
    'reset',

    # decorators
    'chain',
    'ensure',
    'has',
    'inv',
    'post',
    'pre',
    'raises',
    'reason',
    'safe',

    # aliases
    'pure',

    # module level
    'module_load',
    'activate',
]
