# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from __future__ import annotations

from collections.abc import Sequence
from typing import (Union, Optional, Tuple, Any)

import jax
import jax.numpy as jnp

from .._base import (DIMENSIONLESS, Quantity, _return_check_unitless)
from .._misc import set_module_as

__all__ = [

  # math funcs change unit (unary)
  'reciprocal', 'prod', 'product', 'nancumprod', 'nanprod', 'cumprod',
  'cumproduct', 'var', 'nanvar', 'cbrt', 'square', 'sqrt',

  # math funcs change unit (binary)
  'multiply', 'divide', 'power', 'cross', 'ldexp',
  'true_divide', 'floor_divide', 'float_power',
  'divmod', 'convolve',

  # linear algebra
  'dot', 'vdot', 'inner', 'outer', 'kron', 'matmul', 'tensordot',
]


# math funcs change unit (unary)
# ------------------------------


def _fun_change_unit_unary(val_fun, unit_fun, x, *args, **kwargs):
  if isinstance(x, Quantity):
    r = Quantity(val_fun(x.value, *args, **kwargs), dim=unit_fun(x.dim))
    return _return_check_unitless(r)
  return val_fun(x, *args, **kwargs)


@set_module_as('brainunit.math')
def reciprocal(
    x: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.Array]:
  """
  Return the reciprocal of the argument, element-wise.

  Calculates ``1/x``.

  Parameters
  ----------
  x : array_like, Quantity
    Input array.

  Returns
  -------
  y : ndarray, Quantity
    Return array.
    This is a scalar if `x` is a scalar.

    This is a Quantity if the reciprocal of the unit of `x` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.reciprocal, lambda u: u ** -1, x)


@set_module_as('brainunit.math')
def var(
    a: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[Union[int, Sequence[int]]] = None,
    dtype: Optional[Any] = None,
    ddof: int = 0,
    keepdims: bool = False,
    *,
    where: Optional[jax.typing.ArrayLike] = None
) -> Union[Quantity, jax.Array]:
  """
  Compute the variance along the specified axis.

  Returns the variance of the array elements, a measure of the spread of a
  distribution.  The variance is computed for the flattened array by
  default, otherwise over the specified axis.

  Parameters
  ----------
  a : array_like, Quantity
    Array containing numbers whose variance is desired.  If `a` is not an
    array, a conversion is attempted.
  axis : None or int or tuple of ints, optional
    Axis or axes along which the variance is computed.  The default is to
    compute the variance of the flattened array.

    If this is a tuple of ints, a variance is performed over multiple axes,
    instead of a single axis or all the axes as before.
  dtype : data-type, optional
    Type to use in computing the variance.  For arrays of integer type
    the default is `float64`; for arrays of float types it is the same as
    the array type.
  ddof : int, optional
    "Delta Degrees of Freedom": the divisor used in the calculation is
    ``N - ddof``, where ``N`` represents the number of elements. By
    default `ddof` is zero.
  keepdims : bool, optional
    If this is set to True, the axes which are reduced are left
    in the result as dimensions with size one. With this option,
    the result will broadcast correctly against the input array.

    If the default value is passed, then `keepdims` will not be
    passed through to the `var` method of sub-classes of
    `ndarray`, however any non-default value will be.  If the
    sub-class' method does not implement `keepdims` any
    exceptions will be raised.
  where : array_like of bool, optional
      Elements to include in the variance. See `~numpy.ufunc.reduce` for
      details.

  Returns
  -------
  variance : ndarray, quantity, see dtype parameter above
    If ``out=None``, returns a new array containing the variance;
    otherwise, a reference to the output array is returned.

    This is a Quantity if the square of the unit of `a` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.var,
                                lambda u: u ** 2,
                                a,
                                axis=axis,
                                dtype=dtype,
                                ddof=ddof,
                                keepdims=keepdims,
                                where=where)


@set_module_as('brainunit.math')
def nanvar(
    x: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[Union[int, Sequence[int]]] = None,
    dtype: Optional[Any] = None,
    ddof: int = 0,
    keepdims: bool = False,
    where: Optional[jax.typing.ArrayLike] = None
) -> Union[Quantity, jax.Array]:
  """
  Compute the variance along the specified axis, while ignoring NaNs.

  Returns the variance of the array elements, a measure of the spread of
  a distribution.  The variance is computed for the flattened array by
  default, otherwise over the specified axis.

  For all-NaN slices or slices with zero degrees of freedom, NaN is
  returned and a `RuntimeWarning` is raised.

  Parameters
  ----------
  x : array_like, Quantity
    Array containing numbers whose variance is desired.  If `a` is not an
    array, a conversion is attempted.
  axis : {int, tuple of int, None}, optional
    Axis or axes along which the variance is computed.  The default is to compute
    the variance of the flattened array.
  dtype : data-type, optional
    Type to use in computing the variance.  For arrays of integer type
    the default is `float64`; for arrays of float types it is the same as
    the array type.
  ddof : int, optional
    "Delta Degrees of Freedom": the divisor used in the calculation is
    ``N - ddof``, where ``N`` represents the number of non-NaN
    elements. By default `ddof` is zero.
  keepdims : bool, optional
    If this is set to True, the axes which are reduced are left
    in the result as dimensions with size one. With this option,
    the result will broadcast correctly against the original `a`.
  where : array_like of bool, optional
    Elements to include in the variance. See `~numpy.ufunc.reduce` for
    details.

  Returns
  -------
  variance : ndarray, quantity, see dtype parameter above
    If `out` is None, return a new array containing the variance,
    otherwise return a reference to the output array. If ddof is >= the
    number of non-NaN elements in a slice or the slice contains only
    NaNs, then the result for that slice is NaN.

    This is a Quantity if the square of the unit of `a` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.nanvar,
                                lambda u: u ** 2,
                                x,
                                axis=axis,
                                dtype=dtype,
                                ddof=ddof,
                                keepdims=keepdims,
                                where=where)


@set_module_as('brainunit.math')
def sqrt(
    x: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.Array]:
  """
  Compute the square root of each element.

  Parameters
  ----------
  x : array_like, Quantity
    The values whose square-roots are required.

  Returns
  -------
  y : ndarray, quantity
    An array of the same shape as `x`, containing the positive
    square-root of each element in `x`.  If any element in `x` is
    complex, a complex array is returned (and the square-roots of
    negative reals are calculated).  If all of the elements in `x`
    are real, so is `y`, with negative elements returning ``nan``.
    If `out` was provided, `y` is a reference to it.
    This is a scalar if `x` is a scalar.

    This is a Quantity if the square root of the unit of `x` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.sqrt, lambda u: u ** 0.5, x)


@set_module_as('brainunit.math')
def cbrt(
    x: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.Array]:
  """
  Compute the cube root of each element.

  Parameters
  ----------
  x : array_like, Quantity
    The values whose cube-roots are required.

  Returns
  -------
  y : ndarray, quantity
    An array of the same shape as `x`, containing the cube
    cube-root of each element in `x`.
    If `out` was provided, `y` is a reference to it.
    This is a scalar if `x` is a scalar.

    This is a Quantity if the cube root of the unit of `x` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.cbrt, lambda u: u ** (1 / 3), x)


@set_module_as('brainunit.math')
def square(
    x: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.Array]:
  """
  Compute the square of each element.

  Parameters
  ----------
  x : array_like, Quantity
      Input data.

  Returns
  -------
  out : ndarray, quantity or scalar
    Element-wise `x*x`, of the same shape and dtype as `x`.
    This is a scalar if `x` is a scalar.

    This is a Quantity if the square of the unit of `x` is not dimensionless.
  """
  return _fun_change_unit_unary(jnp.square, lambda u: u ** 2, x)


@set_module_as('brainunit.math')
def prod(
    x: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[int] = None,
    dtype: Optional[jax.typing.DTypeLike] = None,
    keepdims: Optional[bool] = False,
    initial: Union[Quantity, jax.typing.ArrayLike] = None,
    where: Union[Quantity, jax.typing.ArrayLike] = None,
    promote_integers: bool = True
) -> Union[Quantity, jax.Array]:
  """
  Return the product of array elements over a given axis.

  Parameters
  ----------
  x : array_like, Quantity
    Input data.
  axis : None or int or tuple of ints, optional
    Axis or axes along which a product is performed.  The default,
    axis=None, will calculate the product of all the elements in the
    input array. If axis is negative it counts from the last to the
    first axis.

    If axis is a tuple of ints, a product is performed on all of the
    axes specified in the tuple instead of a single axis or all the
    axes as before.
  dtype : dtype, optional
    The type of the returned array, as well as of the accumulator in
    which the elements are multiplied.  The dtype of `a` is used by
    default unless `a` has an integer dtype of less precision than the
    default platform integer.  In that case, if `a` is signed then the
    platform integer is used while if `a` is unsigned then an unsigned
    integer of the same precision as the platform integer is used.
  keepdims : bool, optional
    If this is set to True, the axes which are reduced are left in the
    result as dimensions with size one. With this option, the result
    will broadcast correctly against the input array.

    If the default value is passed, then `keepdims` will not be
    passed through to the `prod` method of sub-classes of
    `ndarray`, however any non-default value will be.  If the
    sub-class' method does not implement `keepdims` any
    exceptions will be raised.
  initial : scalar, optional
    The starting value for this product. See `~numpy.ufunc.reduce` for details.
  where : array_like of bool, optional
    Elements to include in the product. See `~numpy.ufunc.reduce` for details.

  Returns
  -------
  product_along_axis : ndarray, see `dtype` parameter above.
    An array shaped as `a` but with the specified axis removed.
    Returns a reference to `out` if specified.

    This is a Quantity if the product of the unit of `x` is not dimensionless.
  """
  if isinstance(x, Quantity):
    return x.prod(axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where,
                  promote_integers=promote_integers)
  else:
    return jnp.prod(x, axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where,
                    promote_integers=promote_integers)


@set_module_as('brainunit.math')
def nanprod(
    x: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[int] = None,
    dtype: Optional[jax.typing.DTypeLike] = None,
    keepdims: bool = False,
    initial: Union[Quantity, jax.typing.ArrayLike] = None,
    where: Union[Quantity, jax.typing.ArrayLike] = None
):
  """
  Return the product of array elements over a given axis treating Not a Numbers (NaNs) as one.

  Parameters
  ----------
  x : array_like, Quantity
    Input data.
  axis : None or int or tuple of ints, optional
    Axis or axes along which a product is performed.  The default,
    axis=None, will calculate the product of all the elements in the
    input array. If axis is negative it counts from the last to the
    first axis.

    If axis is a tuple of ints, a product is performed on all of the
    axes specified in the tuple instead of a single axis or all the
    axes as before.
  dtype : dtype, optional
    The type of the returned array, as well as of the accumulator in
    which the elements are multiplied.  The dtype of `a` is used by
    default unless `a` has an integer dtype of less precision than the
    default platform integer.  In that case, if `a` is signed then the
    platform integer is used while if `a` is unsigned then an unsigned
    integer of the same precision as the platform integer is used.
  out : ndarray, optional
    Alternative output array in which to place the result. It must have
    the same shape as the expected output, but the type of the output
    values will be cast if necessary.
  keepdims : bool, optional
    If this is set to True, the axes which are reduced are left in the
    result as dimensions with size one. With this option, the result
    will broadcast correctly against the input array.

    If the default value is passed, then `keepdims` will not be
    passed through to the `prod` method of sub-classes of
    `ndarray`, however any non-default value will be.  If the
    sub-class' method does not implement `keepdims` any
    exceptions will be raised.
  initial : scalar, optional
    The starting value for this product. See `~numpy.ufunc.reduce` for details.
  where : array_like of bool, optional
    Elements to include in the product. See `~numpy.ufunc.reduce` for details.

  Returns
  -------
  product_along_axis : ndarray, see `dtype` parameter above.
    An array shaped as `a` but with the specified axis removed.
    Returns a reference to `out` if specified.

    This is a Quantity if the product of the unit of `x` is not dimensionless.
  """
  if isinstance(x, Quantity):
    return x.nanprod(axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)
  else:
    return jnp.nanprod(x, axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)


product = prod


@set_module_as('brainunit.math')
def cumprod(
    x: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[int] = None,
    dtype: Optional[jax.typing.DTypeLike] = None
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Return the cumulative product of elements along a given axis.

  Parameters
  ----------
  x : array_like, Quantity
    Input array.
  axis : int, optional
    Axis along which the cumulative product is computed.  By default
    the input is flattened.
  dtype : dtype, optional
    Type of the returned array, as well as of the accumulator in which
    the elements are multiplied.  If *dtype* is not specified, it
    defaults to the dtype of `a`, unless `a` has an integer dtype with
    a precision less than that of the default platform integer.  In
    that case, the default platform integer is used instead.
  out : ndarray, optional
    Alternative output array in which to place the result. It must
    have the same shape and buffer length as the expected output
    but the type of the resulting values will be cast if necessary.

  Returns
  -------
  cumprod : ndarray, quantity
    A new array holding the result is returned unless `out` is
    specified, in which case a reference to out is returned.

    This is a Quantity if the product of the unit of `x` is not dimensionless.
  """
  if isinstance(x, Quantity):
    return x.cumprod(axis=axis, dtype=dtype)
  else:
    return jnp.cumprod(x, axis=axis, dtype=dtype)


@set_module_as('brainunit.math')
def nancumprod(
    x: Union[Quantity, jax.typing.ArrayLike],
    axis: Optional[int] = None,
    dtype: Optional[jax.typing.DTypeLike] = None
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Return the cumulative product of elements along a given axis treating Not a Numbers (NaNs) as one.

  Parameters
  ----------
  x : array_like, Quantity
    Input array.
  axis : int, optional
    Axis along which the cumulative product is computed.  By default
    the input is flattened.
  dtype : dtype, optional
    Type of the returned array, as well as of the accumulator in which
    the elements are multiplied.  If *dtype* is not specified, it
    defaults to the dtype of `a`, unless `a` has an integer dtype with
    a precision less than that of the default platform integer.  In
    that case, the default platform integer is used instead.
  out : ndarray, optional
    Alternative output array in which to place the result. It must
    have the same shape and buffer length as the expected output
    but the type of the resulting values will be cast if necessary.

  Returns
  -------
  cumprod : ndarray, quantity
    A new array holding the result is returned unless `out` is
    specified, in which case a reference to out is returned.

    This is a Quantity if the product of the unit of `x` is not dimensionless.
  """
  if isinstance(x, Quantity):
    return x.nancumprod(axis=axis, dtype=dtype)
  else:
    return jnp.nancumprod(x, axis=axis, dtype=dtype)


cumproduct = cumprod


# math funcs change unit (binary)
# -------------------------------


def _fun_change_unit_binary(val_fun, unit_fun, x, y, *args, **kwargs):
  if isinstance(x, Quantity) and isinstance(y, Quantity):
    return _return_check_unitless(
      Quantity(val_fun(x.value, y.value, *args, **kwargs), dim=unit_fun(x.dim, y.dim))
    )
  elif isinstance(x, Quantity):
    return _return_check_unitless(
      Quantity(val_fun(x.value, y, *args, **kwargs), dim=unit_fun(x.dim, DIMENSIONLESS))
    )
  elif isinstance(y, Quantity):
    return _return_check_unitless(
      Quantity(val_fun(x, y.value, *args, **kwargs), dim=unit_fun(DIMENSIONLESS, y.dim))
    )
  else:
    return val_fun(x, y, *args, **kwargs)


@set_module_as('brainunit.math')
def multiply(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Multiply arguments element-wise.

  Parameters
  ----------
  x, y : array_like, Quantity
    Input arrays to be multiplied.
    If ``x.shape != y.shape``, they must be broadcastable to a common

  Returns
  -------
  out : ndarray, Quantity
    The product of `x` and `y`, element-wise.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the product of the unit of `x` and the unit of `y` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.multiply,
                                 lambda ux, uy: ux * uy,
                                 x, y)


@set_module_as('brainunit.math')
def divide(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Divide arguments element-wise.

  Parameters
  ----------
  x, y : array_like, Quantity
    Input arrays to be divided.
    If ``x.shape != y.shape``, they must be broadcastable to a common

  Returns
  -------
  out : ndarray, Quantity
    The quotient of `x` and `y`, element-wise.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the product of the unit of `x` and the unit of `y` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.divide,
                                 lambda ux, uy: ux / uy,
                                 x, y)


@set_module_as('brainunit.math')
def cross(
    a: Union[Quantity, jax.typing.ArrayLike],
    b: Union[Quantity, jax.typing.ArrayLike],
    axisa: int = -1,
    axisb: int = -1,
    axisc: int = -1,
    axis: Optional[int] = None
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Return the cross product of two (arrays of) vectors.

  The cross product of `a` and `b` in :math:`R^3` is a vector perpendicular
  to both `a` and `b`.  If `a` and `b` are arrays of vectors, the vectors
  are defined by the last axis of `a` and `b` by default, and these axes
  can have dimensions 2 or 3.  Where the dimension of either `a` or `b` is
  2, the third component of the input vector is assumed to be zero and the
  cross product calculated accordingly.  In cases where both input vectors
  have dimension 2, the z-component of the cross product is returned.

  Parameters
  ----------
  a : array_like, Quantity
    Components of the first vector(s).
  b : array_like, Quantity
    Components of the second vector(s).
  axisa : int, optional
    Axis of `a` that defines the vector(s).  By default, the last axis.
  axisb : int, optional
    Axis of `b` that defines the vector(s).  By default, the last axis.
  axisc : int, optional
    Axis of `c` containing the cross product vector(s).  Ignored if
    both input vectors have dimension 2, as the return is scalar.
    By default, the last axis.
  axis : int, optional
    If defined, the axis of `a`, `b` and `c` that defines the vector(s)
    and cross product(s).  Overrides `axisa`, `axisb` and `axisc`.

  Returns
  -------
  c : ndarray, Quantity
    Vector cross product(s).

    This is a Quantity if the cross product of the unit of `a` and the unit of `b` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.cross,
                                 lambda ux, uy: ux * uy,
                                 a, b,
                                 axisa=axisa, axisb=axisb, axisc=axisc, axis=axis)


@set_module_as('brainunit.math')
def ldexp(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: jax.typing.ArrayLike
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Returns x * 2**y, element-wise.

  The mantissas `x` and twos exponents `y` are used to construct
  floating point numbers ``x * 2**y``.

  Parameters
  ----------
  x : array_like, Quantity
    Array of multipliers.
  y : array_like, int
    Array of twos exponents.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out : ndarray, quantity or scalar
    The result of ``x * 2**y``.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the product of the square of the unit of `x` and the unit of `y` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.ldexp,
                                 lambda ux, uy: ux * 2 ** uy,
                                 x, y)


@set_module_as('brainunit.math')
def true_divide(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Returns a true division of the inputs, element-wise.

  Parameters
  ----------
  x : array_like, Quantity
    Dividend array.
  y : array_like, Quantity
    Divisor array.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out : ndarray, quantity or scalar
    The quotient ``x/y``, element-wise.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the division of the unit of `x` and the unit of `y` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.true_divide,
                                 lambda ux, uy: ux / uy,
                                 x, y)


@set_module_as('brainunit.math')
def divmod(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike]
) -> Tuple[Union[Quantity, jax.typing.ArrayLike], Union[Quantity, jax.typing.ArrayLike]]:
  """
  Return element-wise quotient and remainder simultaneously.
  ``bu.divmod(x, y)`` is equivalent to ``(x // y, x % y)``, but faster
  because it avoids redundant work. It is used to implement the Python
  built-in function ``divmod`` on NumPy arrays.

  Parameters
  ----------
  x : array_like, Quantity
    Dividend array.
  y : array_like, Quantity
    Divisor array.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out1 : ndarray, quantity or scalar
    Element-wise quotient resulting from floor division.
    This is a scalar if both `x` and `y` are scalars.
  out2 : ndarray, quantity or scalar
    Element-wise remainder from floor division.
    This is a scalar if both `x` and `y` are scalars.
  """
  if isinstance(x, Quantity) and isinstance(y, Quantity):
    r = jnp.divmod(x.value, y.value)
    return Quantity(r[0], dim=x.dim / y.dim), Quantity(r[1], dim=x.dim)
  elif isinstance(x, Quantity):
    r = jnp.divmod(x.value, y)
    return Quantity(r[0], dim=x.dim / DIMENSIONLESS), Quantity(r[1], dim=x.dim)
  elif isinstance(y, Quantity):
    r = jnp.divmod(x, y.value)
    return Quantity(r[0], dim=DIMENSIONLESS / y.dim), Quantity(r[1], dim=DIMENSIONLESS)
  else:
    return jnp.divmod(x, y)


@set_module_as('brainunit.math')
def convolve(
    a: Union[Quantity, jax.typing.ArrayLike],
    v: Union[Quantity, jax.typing.ArrayLike],
    mode: str = 'full',
    *,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[Quantity, jax.typing.ArrayLike]:
  """
  Returns the discrete, linear convolution of two one-dimensional sequences.

  The convolution operator is often seen in signal processing, where it
  models the effect of a linear time-invariant system on a signal [1]_.  In
  probability theory, the sum of two independent random variables is
  distributed according to the convolution of their individual
  distributions.

  If `v` is longer than `a`, the arrays are swapped before computation.

  Parameters
  ----------
  a : (N,) array_like, Quantity
    First one-dimensional input array.
  v : (M,) array_like, Quantity
    Second one-dimensional input array.
  mode : {'full', 'valid', 'same'}, optional
    'full':
      By default, mode is 'full'.  This returns the convolution
      at each point of overlap, with an output shape of (N+M-1,). At
      the end-points of the convolution, the signals do not overlap
      completely, and boundary effects may be seen.
    'same':
      Mode 'same' returns output of length ``max(M, N)``.  Boundary
      effects are still visible.
    'valid':
      Mode 'valid' returns output of length
      ``max(M, N) - min(M, N) + 1``.  The convolution product is only given
      for points where the signals overlap completely.  Values outside
      the signal boundary have no effect.

  Returns
  -------
  out : ndarray, quantity or scalar
    Discrete, linear convolution of `a` and `v`.
    This is a scalar if both `a` and `v` are scalars.

    This is a Quantity if the convolution of the unit of `a` and the unit of `v` is not dimensionless.
  """
  return _fun_change_unit_binary(
    jnp.convolve,
    lambda ux, uy: ux * uy,
    a, v,
    mode=mode,
    precision=precision,
    preferred_element_type=preferred_element_type
  )


@set_module_as('brainunit.math')
def power(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike],
) -> Union[Quantity, jax.Array]:
  """
  First array elements raised to powers from second array, element-wise.

  Raise each base in `x` to the positionally-corresponding power in
  `y`.  `x` and `y` must be broadcastable to the same shape.

  An integer type raised to a negative integer power will raise a
  ``ValueError``.

  Negative values raised to a non-integral value will return ``nan``.
  To get complex results, cast the input to complex, or specify the
  ``dtype`` to be ``complex`` (see the example below).

  Parameters
  ----------
  x : array_like, Quantity
    The bases.
  y : array_like, Quantity
    The exponents.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out : ndarray, quantity or scalar
    The bases in `x` raised to the exponents in `y`.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the unit of `x` raised to the unit of `y` is not dimensionless.
  """
  if isinstance(x, Quantity):
    if isinstance(y, Quantity):
      assert y.is_unitless, f'{jnp.power.__name__} only supports scalar exponent'
      y = y.value
    return _return_check_unitless(Quantity(jnp.power(x.value, y), dim=x.dim ** y))
  elif isinstance(y, Quantity):
    assert y.is_unitless, f'{jnp.power.__name__} only supports scalar exponent'
    y = y.value
    return _return_check_unitless(Quantity(jnp.power(x, y), dim=x ** y))
  else:
    return jnp.power(x, y)


@set_module_as('brainunit.math')
def floor_divide(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: Union[Quantity, jax.typing.ArrayLike]
) -> Union[Quantity, jax.Array]:
  """
  Return the largest integer smaller or equal to the division of the inputs.
    It is equivalent to the Python ``//`` operator and pairs with the
    Python ``%`` (`remainder`), function so that ``a = a % b + b * (a // b)``
    up to roundoff.

  Parameters
  ----------
  x : array_like, Quantity
    Numerator.
  y : array_like, Quantity
    Denominator.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out : ndarray
    out = floor(`x`/`y`)
    This is a scalar if both `x` and `y` are scalars.
  """
  return _fun_change_unit_binary(jnp.floor_divide, lambda ux, uy: ux / uy, x, y)


@set_module_as('brainunit.math')
def float_power(
    x: Union[Quantity, jax.typing.ArrayLike],
    y: jax.typing.ArrayLike
) -> Union[Quantity, jax.Array]:
  """
  First array elements raised to powers from second array, element-wise.

  Raise each base in `x` to the positionally-corresponding power in `y`.
  `x` and `y` must be broadcastable to the same shape. This differs from
  the power function in that integers, float16, and float32  are promoted to
  floats with a minimum precision of float64 so that the result is always
  inexact.  The intent is that the function will return a usable result for
  negative powers and seldom overflow for positive powers.

  Negative values raised to a non-integral value will return ``nan``.
  To get complex results, cast the input to complex, or specify the
  ``dtype`` to be ``complex`` (see the example below).

  Parameters
  ----------
  x : array_like, Quantity
    The bases.
  y : array_like
    The exponents.
    If ``x.shape != y.shape``, they must be broadcastable to a common
    shape (which becomes the shape of the output).

  Returns
  -------
  out : ndarray
    The bases in `x` raised to the exponents in `y`.
    This is a scalar if both `x` and `y` are scalars.

    This is a Quantity if the unit of `x` raised to the unit of `y` is not dimensionless.
  """
  if isinstance(x, Quantity):
    if isinstance(y, Quantity):
      assert y.is_unitless, f'{jnp.float_power.__name__} only supports scalar exponent'
      y = y.value
    return _return_check_unitless(Quantity(jnp.float_power(x.value, y), dim=x.dim ** y))
  elif isinstance(y, Quantity):
    assert y.is_unitless, f'{jnp.float_power.__name__} only supports scalar exponent'
    y = y.value
    return _return_check_unitless(Quantity(jnp.float_power(x, y), dim=x ** y))
  else:
    return jnp.float_power(x, y)


# linear algebra
# --------------

@set_module_as('brainunit.math')
def dot(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity],
    *,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[jax.Array, Quantity]:
  """
  Dot product of two arrays or quantities.

  Parameters
  ----------
  a : array_like, Quantity
    First argument.
  b : array_like, Quantity
    Second argument.
  precision : either ``None`` (default),
    which means the default precision for the backend, a :class:`~jax.lax.Precision`
    enum value (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``)
    or a tuple of two such values indicating precision of ``a`` and ``b``.
  preferred_element_type : either ``None`` (default)
    which means the default accumulation type for the input types, or a datatype,
    indicating to accumulate results to and return a result with that datatype.

  Returns
  -------
  output : ndarray, Quantity
    array containing the dot product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.dot,
                                 lambda x, y: x * y,
                                 a, b,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type)


@set_module_as('brainunit.math')
def vdot(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity],
    *,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[jax.Array, Quantity]:
  """
  Perform a conjugate multiplication of two 1D vectors.

  Parameters
  ----------
  a : array_like, Quantity
    First argument.
  b : array_like, Quantity
    Second argument.
  precision : either ``None`` (default),
    which means the default precision for the backend, a :class:`~jax.lax.Precision`
    enum value (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``)
    or a tuple of two such values indicating precision of ``a`` and ``b``.
  preferred_element_type : either ``None`` (default)
    which means the default accumulation type for the input types, or a datatype,
    indicating to accumulate results to and return a result with that datatype.

  Returns
  -------
  output : ndarray, Quantity
    array containing the dot product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.vdot,
                                 lambda x, y: x * y,
                                 a, b,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type)


@set_module_as('brainunit.math')
def inner(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity],
    *,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[jax.Array, Quantity]:
  """
  Inner product of two arrays or quantities.

  Parameters
  ----------
  a : array_like, Quantity
    First argument.
  b : array_like, Quantity
    Second argument.
  precision : either ``None`` (default),
    which means the default precision for the backend, a :class:`~jax.lax.Precision`
    enum value (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``)
    or a tuple of two such values indicating precision of ``a`` and ``b``.
  preferred_element_type : either ``None`` (default)
    which means the default accumulation type for the input types, or a datatype,
    indicating to accumulate results to and return a result with that datatype.

  Returns
  -------
  output : ndarray, Quantity
    array containing the inner product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.inner,
                                 lambda x, y: x * y,
                                 a, b,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type)


@set_module_as('brainunit.math')
def outer(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity],
    out: Optional[Any] = None
) -> Union[jax.Array, Quantity]:
  """
  Compute the outer product of two vectors or quantities.

  Parameters
  ----------
  a : array_like, Quantity
    First argument.
  b : array_like, Quantity
    Second argument.
  out : ndarray, optional
    A location into which the result is stored. If provided, it must have a shape that the inputs broadcast to.
    If not provided or None, a freshly-allocated array is returned.

  Returns
  -------
  output : ndarray, Quantity
    array containing the outer product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.outer,
                                 lambda x, y: x * y,
                                 a, b,
                                 out=out)


@set_module_as('brainunit.math')
def kron(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity]
) -> Union[jax.Array, Quantity]:
  """
  Compute the Kronecker product of two arrays or quantities.

  Parameters
  ----------
  a : array_like, Quantity
    First input.
  b : array_like, Quantity
    Second input.

  Returns
  -------
  output : ndarray, Quantity
    Kronecker product of `a` and `b`.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.kron,
                                 lambda x, y: x * y,
                                 a, b)


@set_module_as('brainunit.math')
def matmul(
    a: Union[jax.Array, Quantity],
    b: Union[jax.Array, Quantity],
    *,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[jax.Array, Quantity]:
  """
  Matrix product of two arrays or quantities.

  Parameters
  ----------
  a : array_like, Quantity
    First argument.
  b : array_like, Quantity
    Second argument.
  precision : either ``None`` (default),
    which means the default precision for the backend, a :class:`~jax.lax.Precision`
    enum value (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``)
    or a tuple of two such values indicating precision of ``a`` and ``b``.
  preferred_element_type : either ``None`` (default)
    which means the default accumulation type for the input types, or a datatype,
    indicating to accumulate results to and return a result with that datatype.

  Returns
  -------
  output : ndarray, Quantity
    array containing the matrix product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

    This is a Quantity if the final unit is the product of the unit of `a` and the unit of `b`, else an array.
  """
  return _fun_change_unit_binary(jnp.matmul,
                                 lambda x, y: x * y,
                                 a, b,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type)


@set_module_as('brainunit.math')
def tensordot(
    a: Union[jax.typing.ArrayLike, Quantity],
    b: Union[jax.typing.ArrayLike, Quantity],
    axes: Union[int, Tuple[int, int]] = 2,
    precision: Any = None,
    preferred_element_type: Optional[jax.typing.DTypeLike] = None
) -> Union[jax.Array, Quantity]:
  """
  Compute tensor dot product along specified axes.

  Given two tensors, `a` and `b`, and an array_like object containing
  two array_like objects, ``(a_axes, b_axes)``, sum the products of
  `a`'s and `b`'s elements (components) over the axes specified by
  ``a_axes`` and ``b_axes``. The third argument can be a single non-negative
  integer_like scalar, ``N``; if it is such, then the last ``N`` dimensions
  of `a` and the first ``N`` dimensions of `b` are summed over.

  Parameters
  ----------
  a, b : array_like, Quantity
    Tensors to "dot".

  axes : int or (2,) array_like
    * integer_like
      If an int N, sum over the last N axes of `a` and the first N axes
      of `b` in order. The sizes of the corresponding axes must match.
    * (2,) array_like
      Or, a list of axes to be summed over, first sequence applying to `a`,
      second to `b`. Both elements array_like must be of the same length.
  precision : Optional. Either ``None``, which means the default precision for
    the backend, a :class:`~jax.lax.Precision` enum value
    (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``), a
    string (e.g. 'highest' or 'fastest', see the
    ``jax.default_matmul_precision`` context manager), or a tuple of two
    :class:`~jax.lax.Precision` enums or strings indicating precision of
    ``lhs`` and ``rhs``.
  preferred_element_type : Optional. Either ``None``, which means the default
    accumulation type for the input types, or a datatype, indicating to
    accumulate results to and return a result with that datatype.

  Returns
  -------
  output : ndarray, Quantity
    The tensor dot product of the input.

    This is a quantity if the product of the units of `a` and `b` is not dimensionless.
  """
  return _fun_change_unit_binary(jnp.tensordot,
                                 lambda x, y: x * y,
                                 a, b,
                                 axes=axes,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type)
