from . import linalg

from .laze import (
    shared_intermediates,
    array,
    transpose,
    reshape,
    tensordot,
    einsum,
    trace,
    matmul,
    clip,
    flip,
    sort,
    argsort,
    # binary
    multiply,
    add,
    divide,
    # unary
    sin,
    cos,
    tan,
    arcsin,
    arccos,
    arctan,
    sinh,
    cosh,
    tanh,
    arcsinh,
    arccosh,
    arctanh,
    exp,
    log,
    log2,
    log10,
    conj,
    sign,
    real,
    imag,
    # reductions
    prod,
)
from .laze import abs_ as abs
from .laze import sum_ as sum
from .laze import min_ as min
from .laze import max_ as max

__all__ = (
    'shared_intermediates',
    'linalg',
    'array',
    'transpose',
    'reshape',
    'tensordot',
    'einsum',
    'conj',
    'trace',
    'matmul',
    'clip',
    'flip',
    'sort',
    'argsort',
    # binary
    'multiply',
    'add',
    'divide',
    # unary
    'sin',
    'cos',
    'tan',
    'arcsin',
    'arccos',
    'arctan',
    'sinh',
    'cosh',
    'tanh',
    'arcsinh',
    'arccosh',
    'arctanh',
    'exp',
    'log',
    'log2',
    'log10',
    'conj',
    'sign',
    'abs',
    'real',
    'imag',
    # reductions
    'sum',
    'prod',
    'min',
    'max',
)


try:
    from opt_einsum.backends.dispatch import _aliases
    _aliases['autoray'] = 'autoray.lazearray'
except ImportError:
    pass
