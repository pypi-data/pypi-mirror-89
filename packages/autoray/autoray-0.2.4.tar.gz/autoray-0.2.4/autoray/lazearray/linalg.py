"""
TODO: lstsq, pinv, eigvals, eigvalsh
"""
import operator


from ..autoray import get_lib_fn

from .laze import (
    lazy_cache,
    dtype_real_equiv,
    dtype_complex_equiv,
    find_common_backend,
    find_common_dtype
)


@lazy_cache('linalg.svd')
def svd(a):
    fn_svd = get_lib_fn(a.backend, 'linalg.svd')
    lsvd = a.to(fn_svd, (a,), shape=(3,))
    m, n = a.shape
    k = min(m, n)
    rdtype = dtype_real_equiv(a.dtype)
    lU = lsvd.to(operator.getitem, (lsvd, 0), shape=(m, k))
    ls = lsvd.to(operator.getitem, (lsvd, 1), shape=(k,), dtype=rdtype)
    lV = lsvd.to(operator.getitem, (lsvd, 2), shape=(k, n))
    return lU, ls, lV


@lazy_cache('linalg.qr')
def qr(a):
    lQR = a.to(get_lib_fn(a.backend, 'linalg.qr'), (a,), shape=(2,))
    m, n = a.shape
    k = min(m, n)
    lQ = lQR.to(operator.getitem, (lQR, 0), shape=(m, k))
    lR = lQR.to(operator.getitem, (lQR, 1), shape=(k, n))
    return lQ, lR


@lazy_cache('linalg.eig')
def eig(a):
    fn_eig = get_lib_fn(a.backend, 'linalg.eig')
    leig = a.to(fn_eig, (a,), shape=(2,))
    m = a.shape[0]
    newdtype = dtype_complex_equiv(a.dtype)
    el = leig.to(operator.getitem, (leig, 0), shape=(m,), dtype=newdtype)
    ev = leig.to(operator.getitem, (leig, 1), shape=(m, m), dtype=newdtype)
    return el, ev


@lazy_cache('linalg.eigh')
def eigh(a):
    fn_eigh = get_lib_fn(a.backend, 'linalg.eigh')
    leigh = a.to(fn_eigh, (a,), shape=(2,))
    m = a.shape[0]
    rdtype = dtype_real_equiv(a.dtype)
    el = leigh.to(operator.getitem, (leigh, 0), shape=(m,), dtype=rdtype)
    ev = leigh.to(operator.getitem, (leigh, 1), shape=(m, m))
    return el, ev


@lazy_cache('linalg.inv')
def inv(a):
    fn_inv = get_lib_fn(a.backend, 'linalg.inv')
    return a.to(fn_inv, (a,))


@lazy_cache('linalg.cholesky')
def cholesky(a):
    fn_inv = get_lib_fn(a.backend, 'linalg.cholesky')
    return a.to(fn_inv, (a,))


@lazy_cache('linalg.solve')
def solve(a, b):
    backend = find_common_backend(a.backend, b.backend)
    fn_solve = get_lib_fn('linalg.solve', backend)
    dtype = find_common_dtype((a.dtype, b.dtype), ())
    return b.to(
        backend=backend,
        fn=fn_solve,
        args=(a, b),
        dtype=dtype,
        deps=(a, b),
    )


@lazy_cache('linalg.norm')
def norm(x, order=None):
    fn_inv = get_lib_fn(x.backend, 'linalg.norm')
    newshape = ()
    newdtype = dtype_real_equiv(x.dtype)
    return x.to(fn_inv, (x, order), shape=newshape, dtype=newdtype)
