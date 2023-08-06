import operator
import threading
import functools
import itertools
import contextlib
import collections

import numpy as np

from ..autoray import (
    get_lib_fn,
    infer_backend,
    get_dtype_name,
    register_function,
    astype,
)


_EMPTY_DICT = {}
_eager = False
_strict = False


def get_eager():
    global _eager
    return _eager


def set_eager(b):
    global _eager
    _eager = b


def get_strict():
    global _strict
    return _strict


def set_strict(b):
    global _strict
    _strict = b


@functools.lru_cache(1)
def get_thread_pool_executor():
    from concurrent.futures import ThreadPoolExecutor
    return ThreadPoolExecutor(1)


# _queue = []


# def _process_materializations():
#     import time

#     while True:
#         if _queue:
#             _queue.pop(0).materialize()
#         else:
#             time.sleep(1e-9)


# pool = get_thread_pool_executor()
# pool.submit(_process_materializations)


@functools.lru_cache(1)
def get_dask_client():
    from distributed import get_client
    return get_client()


@functools.lru_cache(1)
def get_ray():
    import ray
    return ray


@functools.lru_cache(2**20)
def get_remote_fn(fn):
    ray = get_ray()

    @ray.remote
    def rfn(*args, **kwargs):
        return fn(*args, **kwargs)

    return rfn


def submit(fn, args, kwargs):
    # compute the real data
    if not _eager:
        return fn(*args, **kwargs)

    elif _eager == 'thread':
        pool = get_thread_pool_executor()
        return pool.submit(fn, *args, **kwargs)

    elif _eager == 'dask':
        pool = get_dask_client()
        return pool.submit(fn, *args, **kwargs)

    elif _eager == 'ray':
        rfn = get_remote_fn(fn)
        return rfn.remote(*args, **kwargs)


def result(x):
    if _eager == 'thread':
        return x.result()
    return x


class LazeArray:

    __slots__ = (
        '_backend',
        '_fn',
        '_args',
        '_kwargs',
        '_shape',
        '_dtype',
        '_deps',
        '_data',
    )

    def __init__(self, backend, fn, args, kwargs, shape, dtype, deps=None):
        self._backend = backend

        self._fn = fn
        self._args = args
        if kwargs is None:
            self._kwargs = _EMPTY_DICT
        else:
            self._kwargs = kwargs

        if deps is None:
            self._deps = (*find_lazy(self._args), *find_lazy(self._kwargs))
        else:
            self._deps = deps

        self._shape = shape
        self._dtype = dtype
        self._data = None

        if _strict:
            if not isinstance(dtype, str):
                raise TypeError
            if not all(isinstance(dep, LazeArray) for dep in self._deps):
                raise TypeError

        if _eager:
            self.materialize()

        # if len(self._deps) > 1:
            # _queue.append(self)

    def to(
        self,
        fn,
        args,
        kwargs=None,
        backend=None,
        shape=None,
        dtype=None,
        deps=None,
    ):
        return LazeArray(
            fn=fn,
            args=args,
            kwargs=kwargs,
            backend=backend if backend is not None else self._backend,
            shape=shape if shape is not None else self.shape,
            dtype=dtype if dtype is not None else self.dtype,
            deps=deps if deps is not None else (self,)
        )

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return len(self._shape)

    @property
    def size(self):
        return functools.reduce(operator.mul, self.shape, 1)

    @property
    def dtype(self):
        return self._dtype

    @property
    def backend(self):
        return self._backend

    @property
    def deps(self):
        return self._deps

    def __getitem__(self, key):
        return getitem(self, key)

    def __mul__(self, other):
        return multiply(self, other)

    def __rmul__(self, other):
        return multiply(self, other)

    def __add__(self, other):
        return add(self, other)

    def __radd__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __rsub__(self, other):
        return sub(other, self)

    def __truediv__(self, other):
        return divide(self, other)

    def __rtruediv__(self, other):
        return divide(other, self)

    def __pow__(self, other):
        return pow_(self, other)

    def __rpow__(self, other):
        return pow_(other, self)

    def __matmul__(self, other):
        return matmul(self, other)

    def __rmatmul__(self, other):
        return matmul(other, self)

    def __abs__(self):
        return abs_(self)

    @property
    def T(self):
        return transpose(self)

    @property
    def H(self):
        return conj(transpose(self))

    def materialize(self):
        if self._data is None:
            # materialize any actual array args
            args = (maybe_materialize(arg) for arg in self._args)
            kwargs = {k: maybe_materialize(v) for k, v in self._kwargs.items()}

            self._data = submit(self._fn, args, kwargs)

            if _strict:
                # check actual resulting array is as promised
                if hasattr(self._data, 'shape'):
                    assert tuple(self.shape) == tuple(self._data.shape)
                    assert infer_backend(self._data) == self.backend
                if hasattr(self._data, 'dtype'):
                    assert self.dtype == self._data.dtype

            # free any references to deps
            self._fn = self._args = self._kwargs = None
            self._deps = ()

        return self._data

    def compute(self):
        queue = [self]
        while queue:
            node = queue[-1]
            need_to_compute = [lz for lz in node.deps if lz._data is None]
            if need_to_compute:
                queue.extend(need_to_compute)
            else:
                node = queue.pop()
                node.materialize()
        return self._data

    def history_max_size(self):
        size = 0
        queue = [self]
        seen = set()
        while queue:
            node = queue.pop()
            size = max(size, node.size)
            queue.extend(nd for nd in node.deps if id(nd) not in seen)
            seen.add(id(node))
        return size

    def __repr__(self):
        return (
            f"<LazeArray(shape={self.shape}, "
            f"dtype={self.dtype}, "
            f"backend={self.backend})>"
        )


def maybe_materialize(x):
    if isinstance(x, LazeArray):
        return result(x.materialize())

    if isinstance(x, tuple):
        return tuple(map(maybe_materialize, x))

    if isinstance(x, list):
        return list(map(maybe_materialize, x))

    if isinstance(x, dict):
        return {k: maybe_materialize(v) for k, v in x.items()}

    return x


def find_lazy(x):
    if isinstance(x, LazeArray):
        yield x
        return

    if isinstance(x, (tuple, list)):
        for subx in x:
            yield from find_lazy(subx)
        return

    if isinstance(x, dict):
        for subx in x.values():
            yield from find_lazy(subx)
        return


_SHARING_STACK = collections.defaultdict(list)


def currently_sharing():
    """Check if we are currently sharing a cache -- thread specific.
    """
    return threading.get_ident() in _SHARING_STACK


def get_sharing_cache():
    """Return the most recent sharing cache -- thread specific.
    """
    return _SHARING_STACK[threading.get_ident()][-1]


def _add_sharing_cache(cache):
    _SHARING_STACK[threading.get_ident()].append(cache)


def _remove_sharing_cache():
    tid = threading.get_ident()
    _SHARING_STACK[tid].pop()
    if not _SHARING_STACK[tid]:
        del _SHARING_STACK[tid]


@contextlib.contextmanager
def shared_intermediates(cache=None):
    """Context in which contract intermediate results are shared.

    Note that intermediate computations will not be garbage collected until
    1. this context exits, and
    2. the yielded cache is garbage collected (if it was captured).

    Parameters
    ----------
    cache : dict
        If specified, a user-stored dict in which intermediate results will
        be stored. This can be used to interleave sharing contexts.

    Returns
    -------
    cache : dict
        A dictionary in which sharing results are stored. If ignored,
        sharing results will be garbage collected when this context is
        exited. This dict can be passed to another context to resume
        sharing.
    """
    if cache is None:
        cache = {}
    _add_sharing_cache(cache)
    try:
        yield cache
    finally:
        _remove_sharing_cache()


def maybe_id(x):
    if hasattr(x, 'shape'):
        return id(x)
    return x


def hash_args_kwargs(fn_name, *args, **kwargs):
    hargs = tuple(map(maybe_id, args))
    if kwargs:
        hkwargs = tuple(sorted((k, maybe_id(v)) for k, v in kwargs.items()))
    else:
        hkwargs = None
    return f"{fn_name}-{hash((hargs, hkwargs))}"


def lazy_cache(fn_name, hasher=None):

    if hasher is None:
        hasher = hash_args_kwargs

    def wrapper(fn):

        @functools.wraps(fn)
        def wrapped(*args, **kwargs):

            if not currently_sharing():
                return fn(*args, **kwargs)

            cache = get_sharing_cache()

            key = hasher(fn_name, *args, **kwargs)
            if key not in cache:
                cache[key] = fn(*args, **kwargs)

            return cache[key]

        return wrapped

    return wrapper


_DTYPES_REAL_EQUIV = {'complex128': 'float64', 'complex64': 'float32'}
_DTYPES_COMPLEX_EQUIV = {'float64': 'complex128', 'float32': 'complex64'}


@functools.lru_cache(16)
def dtype_real_equiv(dtype_name):
    return _DTYPES_REAL_EQUIV.get(dtype_name, dtype_name)


@functools.lru_cache(16)
def dtype_complex_equiv(dtype_name):
    return _DTYPES_COMPLEX_EQUIV.get(dtype_name, dtype_name)


@functools.lru_cache(128)
def find_common_dtype(array_types, scalar_types):
    return np.find_common_type(array_types, scalar_types).name


def find_common_backend(*xs):
    return next(iter(x.backend for x in xs if hasattr(x, 'backend')))


@functools.lru_cache(1024)
def find_broadcast_shape(xshape, yshape):
    xndim = len(xshape)
    yndim = len(yshape)
    if xndim < yndim:
        xshape = (1,) * (yndim - xndim)
    elif yndim < xndim:
        yshape = (1,) * (xndim - yndim)
    return tuple(max(d1, d2) for d1, d2 in zip(xshape, yshape))


# interface

def _identity(x):
    return x


@lazy_cache('array')
def array(x):
    return LazeArray(
        backend=infer_backend(x),
        fn=_identity,
        args=(x,),
        kwargs=None,
        shape=tuple(map(int, x.shape)),
        dtype=get_dtype_name(x),
        deps=(),
    )


@lazy_cache('transpose')
def transpose(a, axes=None):
    if axes is None:
        axes = range(a.ndim)[::-1]
    newshape = tuple(a.shape[i] for i in axes)
    fn_transpose = get_lib_fn(a.backend, 'transpose')

    # check for chaining transpositions
    if a._fn is fn_transpose:
        b = a._args[0]
        if isinstance(b, LazeArray):
            axes_prev = a._args[1]
            axes_chained = tuple(axes_prev[k] for k in axes)
            return b.to(fn_transpose, (b, axes_chained), shape=newshape)

    return a.to(fn_transpose, (a, axes), shape=newshape)


@lazy_cache('reshape')
def _reshape_tuple(a, newshape):
    fn_reshape = get_lib_fn(a.backend, 'reshape')
    return a.to(fn_reshape, (a, newshape), shape=newshape)


@functools.lru_cache(1024)
def find_full_reshape(newshape, size):
    try:
        expand = newshape.index(-1)
        before = newshape[:expand]
        after = newshape[expand + 1:]
        d = size // functools.reduce(
            operator.mul, itertools.chain(before, after), 1)
        return (*before, d, *after)
    except ValueError:
        return newshape


def reshape(a, newshape):
    newshape = find_full_reshape(tuple(newshape), a.size)
    return _reshape_tuple(a, newshape)


def getitem_hasher(_, a, key):
    if not isinstance(key, tuple):
        key = (key,)
    hkey = tuple(
        str(k) if isinstance(k, slice) else
        id(k) if hasattr(k, 'shape') else
        k for k in key
    )
    return f"getitem-{hash((id(a), hkey))}"


@lazy_cache('getitem', hasher=getitem_hasher)
def getitem(a, key):

    deps = (a,)

    if not isinstance(key, tuple):
        key = (key,)

    try:
        # expand ellipsis
        expand = key.index(...)
        ndiff = a.ndim - len(key) + 1
        key = key[:expand] + (slice(None),) * ndiff + key[expand + 1:]
    except ValueError:
        # else pad trailing slices if necessary
        ndiff = a.ndim - len(key)
        if ndiff:
            key = key + (slice(None),) * ndiff

    newshape = []
    for k, d in zip(key, a.shape):
        if isinstance(k, LazeArray):
            newshape.append(k.size)
            deps += (k,)
        elif isinstance(k, slice):
            newshape.append(len(range(d)[k]))
        else:
            try:
                newshape.append(len(k))
            except TypeError:
                pass

    # TODO: np.newaxis == None

    newshape = tuple(newshape)
    return a.to(operator.getitem, (a, key), shape=newshape, deps=deps)


@lazy_cache('tensordot')
def tensordot(a, b, axes=2):

    if isinstance(axes, int):
        axes = (tuple(range(a.ndim - axes, a.ndim)), tuple(range(b.ndim)))

    newshape = (tuple(d for i, d in enumerate(a.shape) if i not in axes[0]) +
                tuple(d for i, d in enumerate(b.shape) if i not in axes[1]))

    newdtype = find_common_dtype((a.dtype, b.dtype), ())
    backend = find_common_backend(a, b)
    fn_tensordot = get_lib_fn(backend, 'tensordot')

    return LazeArray(
        backend=backend,
        fn=fn_tensordot,
        args=(a, b, axes),
        kwargs=None,
        shape=newshape,
        dtype=newdtype,
        deps=tuple(x for x in (a, b) if isinstance(x, LazeArray)),
    )


@lazy_cache('einsum')
def einsum(*operands):
    from opt_einsum.parser import parse_einsum_input

    deps, output, larrays = parse_einsum_input(operands)

    size_dict = {}
    for term, op in zip(deps.split(','), larrays):
        for i, char in enumerate(term):
            size_dict[char] = max(size_dict.get(char, 1), op.shape[i])
    eq = deps + '->' + output
    newshape = tuple(size_dict[char] for char in output)

    backend = find_common_backend(*larrays)
    newdtype = find_common_dtype(tuple(lz.dtype for lz in larrays), ())
    fn_einsum = get_lib_fn(backend, 'einsum')

    return LazeArray(
        backend=backend,
        fn=fn_einsum,
        args=(eq, *larrays),
        kwargs=None,
        shape=newshape,
        dtype=newdtype,
        deps=tuple(x for x in larrays if isinstance(x, LazeArray)),
    )


@lazy_cache('trace')
def trace(a):
    return a.to(
        fn=get_lib_fn(a.backend, 'trace'),
        args=(a,),
        shape=(),
    )


@lazy_cache('matmul')
def matmul(x1, x2):
    backend = find_common_backend(x1, x2)
    newdtype = find_common_dtype((x1.dtype, x2.dtype), ())
    newshape = (*x1.shape[:-1], *x2.shape[1:])
    return LazeArray(
        backend=backend,
        fn=operator.matmul,
        args=(x1, x2),
        kwargs=None,
        shape=newshape,
        dtype=newdtype,
        deps=tuple(x for x in (x1, x2) if isinstance(x, LazeArray)),
    )


@lazy_cache('clip')
def clip(a, a_min, a_max):
    fn_clip = get_lib_fn(a.backend, 'clip')
    return a.to(fn_clip, (a, a_min, a_max))


@lazy_cache('flip')
def flip(a, axis=None):
    fn_flip = get_lib_fn(a.backend, 'flip')
    return a.to(fn_flip, (a, axis))


@lazy_cache('sort')
def sort(a, axis=-1):
    return a.to(get_lib_fn(a.backend, 'sort'), (a, axis))


@lazy_cache('argsort')
def argsort(a, axis=-1):
    return a.to(
        fn=get_lib_fn(a.backend, 'argsort'),
        args=(a, axis),
        dtype='int',
    )


def make_binary_func(name, fn):

    @lazy_cache(name)
    def binary_func(x1, x2):
        newdtype = np.result_type(x1, x2).name
        if not hasattr(x1, 'shape'):
            x1shape = ()
        else:
            x1shape = x1.shape
        if not hasattr(x2, 'shape'):
            x2shape = ()
        else:
            x2shape = x2.shape
        newshape = find_broadcast_shape(x1shape, x2shape)
        return LazeArray(
            backend=find_common_backend(x1, x2),
            fn=fn,
            args=(x1, x2),
            kwargs=None,
            shape=newshape,
            dtype=newdtype,
            deps=tuple(x for x in (x1, x2) if isinstance(x, LazeArray)),
        )

    return binary_func


multiply = make_binary_func('multiply', operator.mul)
add = make_binary_func('add', operator.add)
sub = make_binary_func('sub', operator.sub)
divide = make_binary_func('divide', operator.truediv)
pow_ = make_binary_func('pow', operator.pow)


def make_unary_func(name, to_real=False):

    @lazy_cache(name)
    def unary_func(x):

        if to_real:
            newdtype = dtype_real_equiv(x.dtype)
        else:
            newdtype = None

        return x.to(
            fn=get_lib_fn(x.backend, name),
            args=(x,),
            dtype=newdtype,
        )

    return unary_func


sin = make_unary_func('sin')
cos = make_unary_func('cos')
tan = make_unary_func('tan')
arcsin = make_unary_func('arcsin')
arccos = make_unary_func('arccos')
arctan = make_unary_func('arctan')
sinh = make_unary_func('sinh')
cosh = make_unary_func('cosh')
tanh = make_unary_func('tanh')
arcsinh = make_unary_func('arcsinh')
arccosh = make_unary_func('arccosh')
arctanh = make_unary_func('arctanh')
exp = make_unary_func('exp')
log = make_unary_func('log')
log2 = make_unary_func('log2')
log10 = make_unary_func('log10')
conj = make_unary_func('conj')
sign = make_unary_func('sign')
abs_ = make_unary_func('abs', to_real=True)
real = make_unary_func('real', to_real=True)
imag = make_unary_func('imag', to_real=True)


def make_reduction_func(name):

    @lazy_cache(name)
    def reduction_func(a, axis=None):
        nd = a.ndim
        if axis is None:
            axis = tuple(range(nd))
        elif not hasattr(axis, '__len__'):
            axis = (axis,)
        axis = tuple(nd - i if i < 0 else i for i in axis)

        newshape = tuple(d for i, d in enumerate(a.shape) if i not in axis)
        return a.to(
            fn=get_lib_fn(a.backend, name),
            args=(a, axis),
            shape=newshape,
        )

    return reduction_func


sum_ = make_reduction_func('sum')
prod = make_reduction_func('prod')
min_ = make_reduction_func('min')
max_ = make_reduction_func('max')

# stack, allclose, complex, diag
# dot, vdot, kron, inner, outer
# pad, eye
# squeeze, expand_dims
# to_numpy


# ---------------------------- autoray specials ----------------------------- #

def lazy_get_dtype_name(x):
    return x.dtype


@lazy_cache('astype')
def lazy_astype(x, dtype_name):
    return x.to(
        fn=astype,
        args=(x, dtype_name),
        dtype=dtype_name,
    )


register_function('autoray', 'get_dtype_name', lazy_get_dtype_name)
register_function('autoray', 'astype', lazy_astype)
