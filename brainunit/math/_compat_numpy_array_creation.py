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

from collections.abc import Sequence
from typing import (Union, Optional, Any)

import jax
import jax.numpy as jnp
import numpy as np
from jax import Array

from brainunit._misc import set_module_as
from .._base import (
  DIMENSIONLESS,
  Quantity,
  Unit,
  fail_for_dimension_mismatch,
  is_unitless,
)

__all__ = [
  # array creation
  'full', 'full_like', 'eye', 'identity', 'diag', 'tri', 'tril', 'triu',
  'empty', 'empty_like', 'ones', 'ones_like', 'zeros', 'zeros_like',
  'array', 'asarray', 'arange', 'linspace', 'logspace', 'fill_diagonal',
  'array_split', 'meshgrid', 'vander',
]


@set_module_as('brainunit.math')
def full(
    shape: Sequence[int],
    fill_value: Union[Quantity, int, float],
    dtype: Optional[Any] = None,
) -> Union[Array, Quantity]:
  """
  Returns a quantity of `shape`, filled with `fill_value` if `fill_value` is a Quantity.
  else return an array of `shape` filled with `fill_value`.

  Parameters
  ----------
  shape : int or sequence of ints
    Shape of the new array, e.g., ``(2, 3)`` or ``2``.
  fill_value : scalar, array_like or Quantity
      Fill value.
  dtype : data-type, optional
    The desired data-type for the array  The default, None, means ``np.array(fill_value).dtype`

  Returns
  -------
  out : quantity or ndarray
    Quantity with the given shape if `fill_value` is a Quantity, else an array.
    Array of `fill_value` with the given shape, dtype, and order.
  """
  if isinstance(fill_value, Quantity):
    return Quantity(jnp.full(shape, fill_value.value, dtype=dtype), dim=fill_value.dim)
  return jnp.full(shape, fill_value, dtype=dtype)


@set_module_as('brainunit.math')
def eye(
    N: int,
    M: Optional[int] = None,
    k: int = 0,
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None,
    order: str = 'C',
) -> Union[Array, Quantity]:
  """
  Returns a 2-D quantity or array of `shape` and `unit` with ones on the diagonal and zeros elsewhere.

  Parameters
  ----------
  N : int
    Number of rows in the output.
  M : int, optional
    Number of columns in the output. If None, defaults to `N`.
  k : int, optional
    Index of the diagonal: 0 (the default) refers to the main diagonal,
    a positive value refers to an upper diagonal, and a negative value
    to a lower diagonal.
  dtype : data-type, optional
    Data-type of the returned array.
  unit : Unit, optional
    Unit of the returned Quantity.
  order : {'C', 'F'}, optional
      Whether the output should be stored in row-major (C-style) or
      column-major (Fortran-style) order in memory.

  Returns
  -------
  I : quantity or ndarray of shape (N,M)
    An array where all elements are equal to zero, except for the `k`-th
    diagonal, whose values are equal to one.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.eye(N, M, k, dtype=dtype) * unit
  else:
    return jnp.eye(N, M, k, dtype=dtype)


@set_module_as('brainunit.math')
def identity(
    n: int,
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None
) -> Union[Array, Quantity]:
  """
  Return the identity Quantity or array.

  The identity array is a square array with ones on
  the main diagonal.

  Parameters
  ----------
  n : int
    Number of rows (and columns) in `n` x `n` output.
  dtype : data-type, optional
    Data-type of the output.  Defaults to ``float``.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    `n` x `n` quantity or array with its main diagonal set to one,
    and all other elements 0.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.identity(n, dtype=dtype) * unit
  else:
    return jnp.identity(n, dtype=dtype)


@set_module_as('brainunit.math')
def tri(
    N: int,
    M: Optional[int] = None,
    k: int = 0,
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None
) -> Union[Array, Quantity]:
  """
  A quantity or an array with ones at and below the given diagonal and zeros elsewhere.

  Parameters
  ----------
  N : int
    Number of rows in the array.
  M : int, optional
    Number of columns in the array.
    By default, `M` is taken equal to `N`.
  k : int, optional
    The sub-diagonal at and below which the array is filled.
    `k` = 0 is the main diagonal, while `k` < 0 is below it,
    and `k` > 0 is above.  The default is 0.
  dtype : dtype, optional
    Data type of the returned array.  The default is float.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  tri : quantity or ndarray of shape (N, M)
    quantity or array with its lower triangle filled with ones and zero elsewhere;
    in other words ``T[i,j] == 1`` for ``j <= i + k``, 0 otherwise.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.tri(N, M, k, dtype=dtype) * unit
  else:
    return jnp.tri(N, M, k, dtype=dtype)


@set_module_as('brainunit.math')
def empty(
    shape: Sequence[int],
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None
) -> Union[Array, Quantity]:
  """
  Return a new quantity or array of given shape and type, without initializing entries.

  Parameters
  ----------
  shape : sequence of int
    Shape of the empty quantity or array.
  dtype : data-type, optional
    Data-type of the output.  Defaults to ``float``.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    quantity or array of uninitialized (arbitrary) data of the given shape, dtype, and order.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.empty(shape, dtype=dtype) * unit
  else:
    return jnp.empty(shape, dtype=dtype)


@set_module_as('brainunit.math')
def ones(
    shape: Sequence[int],
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None
) -> Union[Array, Quantity]:
  """
  Returns a new quantity or array of given shape and type, filled with ones.

  Parameters
  ----------
  shape : sequence of int
    Shape of the new quantity or array.
  dtype : data-type, optional
    The desired data-type for the array.  Default is `float`.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Array of ones with the given shape, dtype, and order.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.ones(shape, dtype=dtype) * unit
  else:
    return jnp.ones(shape, dtype=dtype)


@set_module_as('brainunit.math')
def zeros(
    shape: Sequence[int],
    dtype: Optional[Any] = None,
    unit: Optional[Unit] = None
) -> Union[Array, Quantity]:
  """
  Returns a new quantity or array of given shape and type, filled with zeros.

  Parameters
  ----------
  shape : sequence of int
    Shape of the new quantity or array.
  dtype : data-type, optional
    The desired data-type for the array.  Default is `float`.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Array of zeros with the given shape, dtype, and order.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
    return jnp.zeros(shape, dtype=dtype) * unit
  else:
    return jnp.zeros(shape, dtype=dtype)


@set_module_as('brainunit.math')
def full_like(
    a: Union[Quantity, jax.typing.ArrayLike],
    fill_value: Union[Quantity, jax.typing.ArrayLike],
    dtype: Optional[jax.typing.DTypeLike] = None,
    shape: Any = None
) -> Union[Quantity, jax.Array]:
  """
  Return a new quantity or array with the same shape and type as a given array or quantity, filled with `fill_value`.

  Parameters
  ----------
  a : quantity or ndarray
    The shape and data-type of `a` define these same attributes of the returned quantity or array.
  fill_value : quantity or ndarray
    Value to fill the new quantity or array with.
  dtype : data-type, optional
    Overrides the data type of the result.
  shape : sequence of int, optional
    Overrides the shape of the result. If `shape` is not given, the shape of `a` is used.

  Returns
  -------
  out : quantity or ndarray
    New quantity or array with the same shape and type as `a`, filled with `fill_value`.
  """
  if isinstance(fill_value, Quantity):
    if isinstance(a, Quantity):
      fail_for_dimension_mismatch(a, fill_value, error_message="a and fill_value have to have the same units.")
      return Quantity(jnp.full_like(a.value, fill_value.value, dtype=dtype, shape=shape),
                      dim=a.dim)
    else:
      return Quantity(jnp.full_like(a, fill_value.value, dtype=dtype, shape=shape),
                      dim=fill_value.dim)
  else:
    if isinstance(a, Quantity):
      return jnp.full_like(a.value, fill_value, dtype=dtype, shape=shape)
    else:
      return jnp.full_like(a, fill_value, dtype=dtype, shape=shape)


@set_module_as('brainunit.math')
def diag(
    v: Union[Quantity, jax.typing.ArrayLike],
    k: int = 0,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Extract a diagonal or construct a diagonal array.

  Parameters
  ----------
  v : quantity or ndarray
    If `a` is a 1-D array, `diag` constructs a 2-D array with `v` on the `k`-th diagonal.
    If `a` is a 2-D array, `diag` extracts the `k`-th diagonal and returns a 1-D array.
  k : int, optional
    Diagonal in question. The default is 0. Use `k>0` for diagonals above the main diagonal, and `k<0` for diagonals
    below the main diagonal.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    The extracted diagonal or constructed diagonal array.
  """
  if isinstance(v, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      fail_for_dimension_mismatch(v, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.diag(v.value, k=k), dim=v.dim)
  elif isinstance(v, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      return jnp.diag(v, k=k) * unit
    else:
      return jnp.diag(v, k=k)
  else:
    return jnp.diag(v, k=k)


@set_module_as('brainunit.math')
def tril(
    m: Union[Quantity, jax.typing.ArrayLike],
    k: int = 0,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Lower triangle of an array.

  Return a copy of a matrix with the elements above the `k`-th diagonal zeroed.
  For quantities or arrays with ``ndim`` exceeding 2, `tril` will apply to the final two axes.

  Parameters
  ----------
  m : quantity or ndarray
    Input array.
  k : int, optional
    Diagonal above which to zero elements. `k = 0` is the main diagonal, `k < 0` is below it, and `k > 0` is above.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Lower triangle of `m`, of the same shape and data-type as `m`.
  """
  if isinstance(m, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      fail_for_dimension_mismatch(m, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.tril(m.value, k=k), dim=m.dim)
  elif isinstance(m, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      return jnp.tril(m, k=k) * unit
    else:
      return jnp.tril(m, k=k)
  else:
    return jnp.tril(m, k=k)


@set_module_as('brainunit.math')
def triu(
    m: Union[Quantity, jax.typing.ArrayLike],
    k: int = 0,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Upper triangle of a quantity or an array.

  Return a copy of an array with the elements below the `k`-th diagonal
  zeroed. For arrays with ``ndim`` exceeding 2, `triu` will apply to the
  final two axes.

  Please refer to the documentation for `tril` for further details.

  See Also
  --------
  tril : lower triangle of an array
  """
  if isinstance(m, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      fail_for_dimension_mismatch(m, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.triu(m.value, k=k), dim=m.dim)
  elif isinstance(m, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
      return jnp.triu(m, k=k) * unit
    else:
      return jnp.triu(m, k=k)
  else:
    return jnp.triu(m, k=k)


@set_module_as('brainunit.math')
def empty_like(
    prototype: Union[Quantity, jax.typing.ArrayLike],
    dtype: Optional[jax.typing.DTypeLike] = None,
    shape: Any = None,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Return a new quantity or array with the same shape and type as a given array.

  Parameters
  ----------
  prototype : quantity or ndarray
    The shape and data-type of `prototype` define these same attributes of the returned array.
  dtype : data-type, optional
    Overrides the data type of the result.
  shape : int or tuple of ints, optional
    Overrides the shape of the result. If not given, `prototype.shape` is used.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Array of uninitialized (arbitrary) data with the same shape and type as `prototype`.
  """
  if isinstance(prototype, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit)
      fail_for_dimension_mismatch(prototype, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.empty_like(prototype.value, dtype=dtype), dim=prototype.dim)
  elif isinstance(prototype, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit)
      return jnp.empty_like(prototype, dtype=dtype, shape=shape) * unit
    else:
      return jnp.empty_like(prototype, dtype=dtype, shape=shape)
  else:
    return jnp.empty_like(prototype, dtype=dtype, shape=shape)


@set_module_as('brainunit.math')
def ones_like(
    a: Union[Quantity, jax.typing.ArrayLike],
    dtype: Optional[jax.typing.DTypeLike] = None,
    shape: Any = None,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Return a quantity or an array of ones with the same shape and type as a given array.

  Parameters
  ----------
  a : quantity or ndarray
    The shape and data-type of `a` define these same attributes of the returned array.
  dtype : data-type, optional
    Overrides the data type of the result.
  shape : int or tuple of ints, optional
    Overrides the shape of the result. If not given, `a.shape` is used.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Array of ones with the same shape and type as `a`.
  """
  if isinstance(a, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit)
      fail_for_dimension_mismatch(a, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.ones_like(a.value, dtype=dtype, shape=shape), dim=a.dim)
  elif isinstance(a, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit)
      return jnp.ones_like(a, dtype=dtype, shape=shape) * unit
    else:
      return jnp.ones_like(a, dtype=dtype, shape=shape)
  else:
    return jnp.ones_like(a, dtype=dtype, shape=shape)


@set_module_as('brainunit.math')
def zeros_like(
    a: Union[Quantity, jax.typing.ArrayLike],
    dtype: Optional[jax.typing.DTypeLike] = None,
    shape: Any = None,
    unit: Optional[Unit] = None
) -> Union[Quantity, jax.Array]:
  """
  Return a quantity or an array of zeros with the same shape and type as a given array.

  Parameters
  ----------
  a : quantity or ndarray
    The shape and data-type of `a` define these same attributes of the returned array.
  dtype : data-type, optional
    Overrides the data type of the result.
  shape : int or tuple of ints, optional
    Overrides the shape of the result. If not given, `a.shape` is used.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or ndarray
    Array of zeros with the same shape and type as `a`.
  """
  if isinstance(a, Quantity):
    if unit is not None:
      assert isinstance(unit, Unit)
      fail_for_dimension_mismatch(a, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.zeros_like(a.value, dtype=dtype, shape=shape), dim=a.dim)
  elif isinstance(a, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit)
      return jnp.zeros_like(a, dtype=dtype, shape=shape) * unit
    else:
      return jnp.zeros_like(a, dtype=dtype, shape=shape)
  else:
    return jnp.zeros_like(a, dtype=dtype, shape=shape)


@set_module_as('brainunit.math')
def asarray(
    a: Union[Quantity, jax.typing.ArrayLike, Sequence[Quantity], Sequence[jax.typing.ArrayLike]],
    dtype: Optional[jax.typing.DTypeLike] = None,
    order: Optional[str] = None,
    unit: Optional[Unit] = None,
) -> Union[Quantity, jax.Array]:
  """
  Convert the input to a quantity or array.

  If unit is provided, the input will be checked whether it has the same unit as the provided unit.
  (If they have same dimension but different magnitude, the input will be converted to the provided unit.)
  If unit is not provided, the input will be converted to an array.

  Parameters
  ----------
  a : quantity, ndarray, list[Quantity], list[ndarray]
    Input data, in any form that can be converted to an array.
  dtype : data-type, optional
    By default, the data-type is inferred from the input data.
  order : {'C', 'F', 'A', 'K'}, optional
    Whether to use row-major (C-style) or column-major (Fortran-style) memory representation.
    Defaults to 'K', which means that the memory layout is used in the order the array elements are stored in memory.
  unit : Unit, optional
    Unit of the returned Quantity.

  Returns
  -------
  out : quantity or array
    Array interpretation of `a`. No copy is made if the input is already an array.
  """
  if unit is not None:
    assert isinstance(unit, Unit), f'unit must be an instance of Unit, got {type(unit)}'
  if isinstance(a, Quantity):
    if unit is not None:
      fail_for_dimension_mismatch(a, unit, error_message="a and unit have to have the same units.")
    return Quantity(jnp.asarray(a.value, dtype=dtype, order=order), dim=a.dim)
  elif isinstance(a, (jax.Array, np.ndarray)):
    if unit is not None:
      assert isinstance(unit, Unit)
      return jnp.asarray(a, dtype=dtype, order=order) * unit
    else:
      return jnp.asarray(a, dtype=dtype, order=order)
    # list[Quantity]
  elif isinstance(a, Sequence):
    leaves, tree = jax.tree.flatten(a, is_leaf=lambda x: isinstance(x, Quantity))
    if all([isinstance(leaf, Quantity) for leaf in leaves]):
      # check all elements have the same unit
      if any(x.dim != leaves[0].dim for x in leaves):
        raise ValueError('Units do not match for asarray operation.')
      values = jax.tree.unflatten(tree, [x.value for x in a])
      if unit is not None:
        fail_for_dimension_mismatch(a[0], unit, error_message="a and unit have to have the same units.")
      unit = a[0].dim
      # Convert the values to a jnp.ndarray and create a Quantity object
      return Quantity(jnp.asarray(values, dtype=dtype, order=order), dim=unit)
    else:
      values = jax.tree.unflatten(tree, leaves)
      val = jnp.asarray(values, dtype=dtype, order=order)
      if unit is not None:
        return val * unit
      else:
        return val
  else:
    raise TypeError('Invalid input type for asarray.')


array = asarray


@set_module_as('brainunit.math')
def arange(
    start: Union[Quantity, jax.typing.ArrayLike] = None,
    stop: Optional[Union[Quantity, jax.typing.ArrayLike]] = None,
    step: Optional[Union[Quantity, jax.typing.ArrayLike]] = None,
    dtype: Optional[jax.typing.DTypeLike] = None
) -> Union[Quantity, jax.Array]:
  """
  Return evenly spaced values within a given interval.

  Parameters
  ----------
  start : Quantity or array, optional
      Start of the interval. The interval includes this value. The default start value is 0.
  stop : Quantity or array
      End of the interval. The interval does not include this value, except in some cases where `step` is not an integer
      and floating point round-off affects the length of `out`.
  step : Quantity or array, optional
      Spacing between values. For any output `out`, this is the distance between two adjacent values, `out[i+1] - out[i]`.
      The default step size is 1.
  dtype : data-type, optional
      The type of the output array. If `dtype` is not given, infer the data type from the other input arguments.

  Returns
  -------
  out : quantity or array
      Array of evenly spaced values.
  """

  arg_len = len([x for x in [start, stop, step] if x is not None])

  if arg_len == 1:
    if stop is not None:
      raise TypeError("Duplicate definition of 'stop'")
    stop = start
    start = 0
  elif arg_len == 2:
    if start is not None and stop is None:
      stop = start
      start = 0

  elif arg_len > 3:
    raise TypeError("Need between 1 and 3 non-keyword arguments")

  # default values
  if start is None:
    start = 0
  if step is None:
    step = 1

  if stop is None:
    raise TypeError("Missing stop argument.")
  if stop is not None and not is_unitless(stop):
    start = Quantity(start, dim=stop.dim)

  fail_for_dimension_mismatch(
    start,
    stop,
    error_message="Start value {start} and stop value {stop} have to have the same units.",
    start=start,
    stop=stop,
  )
  fail_for_dimension_mismatch(
    stop,
    step,
    error_message="Stop value {stop} and step value {step} have to have the same units.",
    stop=stop,
    step=step,
  )

  unit = getattr(stop, "dim", DIMENSIONLESS)

  if start == 0:
    return Quantity(
      jnp.arange(
        start=start.value if isinstance(start, Quantity) else jnp.asarray(start),
        stop=stop.value if isinstance(stop, Quantity) else jnp.asarray(stop),
        step=step.value if isinstance(step, Quantity) else jnp.asarray(step),
        dtype=dtype,
      ),
      dim=unit,
    )
  else:
    return Quantity(
      jnp.arange(
        start.value if isinstance(start, Quantity) else jnp.asarray(start),
        stop=stop.value if isinstance(stop, Quantity) else jnp.asarray(stop),
        step=step.value if isinstance(step, Quantity) else jnp.asarray(step),
        dtype=dtype,
      ),
      dim=unit,
    )


@set_module_as('brainunit.math')
def linspace(
    start: Union[Quantity, jax.typing.ArrayLike],
    stop: Union[Quantity, jax.typing.ArrayLike],
    num: int = 50,
    endpoint: Optional[bool] = True,
    retstep: Optional[bool] = False,
    dtype: Optional[jax.typing.DTypeLike] = None
) -> Union[Quantity, jax.Array]:
  """
  Return evenly spaced numbers over a specified interval.

  Returns `num` evenly spaced samples, calculated over the interval [`start`, `stop`].
  The endpoint of the interval can optionally be excluded.

  Parameters
  ----------
  start : Quantity or array
    The starting value of the sequence.
  stop : Quantity or array
    The end value of the sequence.
  num : int, optional
    Number of samples to generate. Default is 50.
  endpoint : bool, optional
    If True, `stop` is the last sample. Otherwise, it is not included. Default is True.
  retstep : bool, optional
    If True, return (`samples`, `step`), where `step` is the spacing between samples.
  dtype : data-type, optional
    The type of the output array. If `dtype` is not given, infer the data type from the other input arguments.

  Returns
  -------
  samples : quantity or array
    There are `num` equally spaced samples in the closed interval [`start`, `stop`] or the half-open interval [`start`, `stop`).
  """
  fail_for_dimension_mismatch(
    start,
    stop,
    error_message="Start value {start} and stop value {stop} have to have the same units.",
    start=start,
    stop=stop,
  )
  unit = getattr(start, "dim", DIMENSIONLESS)
  start = start.value if isinstance(start, Quantity) else start
  stop = stop.value if isinstance(stop, Quantity) else stop

  result = jnp.linspace(start, stop, num=num, endpoint=endpoint, retstep=retstep, dtype=dtype)
  return Quantity(result, dim=unit)


@set_module_as('brainunit.math')
def logspace(start: Union[Quantity, jax.typing.ArrayLike],
             stop: Union[Quantity, jax.typing.ArrayLike],
             num: Optional[int] = 50,
             endpoint: Optional[bool] = True,
             base: Optional[float] = 10.0,
             dtype: Optional[jax.typing.DTypeLike] = None):
  """
  Return numbers spaced evenly on a log scale.

  In linear space, the sequence starts at `base ** start` (`base` to the power of `start`) and ends with `base ** stop` in `num` steps.

  Parameters
  ----------
  start : Quantity or array
    The starting value of the sequence.
  stop : Quantity or array
    The end value of the sequence.
  num : int, optional
    Number of samples to generate. Default is 50.
  endpoint : bool, optional
    If True, `stop` is the last sample. Otherwise, it is not included. Default is True.
  base : float, optional
    The base of the log space. The step size between the elements in `ln(samples)` is `base`.
  dtype : data-type, optional
    The type of the output array. If `dtype` is not given, infer the data type from the other input arguments.

  Returns
  -------
  samples : quantity or array
    There are `num` equally spaced samples in the closed interval [`start`, `stop`] or the half-open interval [`start`, `stop`).
  """
  fail_for_dimension_mismatch(
    start,
    stop,
    error_message="Start value {start} and stop value {stop} have to have the same units.",
    start=start,
    stop=stop,
  )
  unit = getattr(start, "dim", DIMENSIONLESS)
  start = start.value if isinstance(start, Quantity) else start
  stop = stop.value if isinstance(stop, Quantity) else stop

  result = jnp.logspace(start, stop, num=num, endpoint=endpoint, base=base, dtype=dtype)
  return Quantity(result, dim=unit)


@set_module_as('brainunit.math')
def fill_diagonal(a: Union[Quantity, jax.typing.ArrayLike],
                  val: Union[Quantity, jax.typing.ArrayLike],
                  wrap: Optional[bool] = False,
                  inplace: Optional[bool] = False) -> Union[Quantity, jax.Array]:
  """
  Fill the main diagonal of the given array of any dimensionality.

  For an array `a` with `a.ndim >= 2`, the diagonal is the list of locations with indices `a[i, i, ..., i]`
  all identical.

  Parameters
  ----------
  a : Quantity or array
    Array in which to fill the diagonal.
  val : Quantity or array
    Value to be written on the diagonal. Its type must be compatible with that of the array a.
  wrap : bool, optional
    For tall matrices in NumPy version 1.6.2 and earlier, the matrix is considered "tall" if `a.shape[0] > a.shape[1]`.
    If `wrap` is True, the diagonal is "wrapped" after `a.shape[1]` and continues in the first column.
  inplace : bool, optional
    If True, the diagonal is filled in-place. Default is False.

  Returns
  -------
  out : Quantity or array
    The input array with the diagonal filled.
  """
  if isinstance(val, Quantity):
    if isinstance(a, Quantity):
      fail_for_dimension_mismatch(a, val, error_message="Array and value have to have the same units.")
      return Quantity(jnp.fill_diagonal(a.value, val.value, wrap, inplace=inplace), dim=a.dim)
    else:
      return Quantity(jnp.fill_diagonal(a, val.value, wrap, inplace=inplace), dim=val.dim)
  else:
    if isinstance(a, Quantity):
      return jnp.fill_diagonal(a.value, val, wrap, inplace=inplace)
    else:
      return jnp.fill_diagonal(a, val, wrap, inplace=inplace)


@set_module_as('brainunit.math')
def array_split(
    ary: Union[Quantity, jax.typing.ArrayLike],
    indices_or_sections: Union[int, jax.typing.ArrayLike],
    axis: Optional[int] = 0
) -> Union[list[Quantity], list[Array]]:
  """
  Split an array into multiple sub-arrays.

  Parameters
  ----------
  ary : Quantity or array
    Array to be divided into sub-arrays.
  indices_or_sections : int or 1-D array
    If `indices_or_sections` is an integer, `ary` is divided into `indices_or_sections` sub-arrays along `axis`.
    If such a split is not possible, an error is raised.
    If `indices_or_sections` is a 1-D array of sorted integers, the entries indicate where along `axis` the array is split.
  axis : int, optional
    The axis along which to split, default is 0.

  Returns
  -------
  sub-arrays : list of Quantity or list of array
    A list of sub-arrays.
  """
  if isinstance(ary, Quantity):
    return [Quantity(x, dim=ary.dim) for x in jnp.array_split(ary.value, indices_or_sections, axis)]
  elif isinstance(ary, (jax.Array, np.ndarray)):
    return jnp.array_split(ary, indices_or_sections, axis)
  else:
    raise ValueError(f'Unsupported type: {type(ary)} for array_split')


@set_module_as('brainunit.math')
def meshgrid(
    *xi: Union[Quantity, jax.typing.ArrayLike],
    copy: Optional[bool] = True,
    sparse: Optional[bool] = False,
    indexing: Optional[str] = 'xy'
) -> Union[list[Quantity], list[Array]]:
  """
  Return coordinate matrices from coordinate vectors.

  Make N-D coordinate arrays for vectorized evaluations of N-D scalar/vector fields over N-D grids,
  given one-dimensional coordinate arrays x1, x2,..., xn.

  Parameters
  ----------
  xi : Quantity or array
    1-D arrays representing the coordinates of a grid.
  copy : bool, optional
    If True (default), the returned arrays are copies. If False, the view is returned.
  sparse : bool, optional
    If True, return a sparse grid (meshgrid) instead of a dense grid.
  indexing : {'xy', 'ij'}, optional
    Cartesian ('xy', default) or matrix ('ij') indexing of output.

  Returns
  -------
  X1, X2,..., XN : Quantity or array
    For vectors x1, x2,..., 'xn' with lengths Ni=len(xi), return (N1, N2, N3,..., Nn) shaped arrays if indexing='ij'
    or (N2, N1, N3,..., Nn) shaped arrays if indexing='xy' with the elements of xi repeated to fill the matrix along
    the first dimension for x1, the second for x2 and so on.
  """
  from builtins import all as origin_all
  if origin_all(isinstance(x, Quantity) for x in xi):
    fail_for_dimension_mismatch(*xi)
    return [Quantity(x, dim=xi[0].dim) for x in
            jnp.meshgrid(*[x.value for x in xi], copy=copy, sparse=sparse, indexing=indexing)]
  elif origin_all(isinstance(x, (jax.Array, np.ndarray)) for x in xi):
    return jnp.meshgrid(*xi, copy=copy, sparse=sparse, indexing=indexing)
  else:
    raise ValueError(f'Unsupported types : {type(xi)} for meshgrid')


@set_module_as('brainunit.math')
def vander(
    x: Union[Quantity, jax.typing.ArrayLike],
    N: Optional[bool] = None,
    increasing: Optional[bool] = False
) -> Union[Quantity, jax.Array]:
  """
  Generate a Vandermonde matrix.

  The Vandermonde matrix is a matrix with the terms of a geometric progression in each row.
  The geometric progression is defined by the vector `x` and the number of columns `N`.

  Parameters
  ----------
  x : Quantity or array
    1-D input array.
  N : int, optional
    Number of columns in the output. If `N` is not specified, a square array is returned (N = len(x)).
  increasing : bool, optional
    Order of the powers of the columns. If True, the powers increase from left to right, if False (the default),
    they are reversed.

  Returns
  -------
  out : Quantity or array
    Vandermonde matrix. If `increasing` is False, the first column is `x^(N-1)`, the second `x^(N-2)` and so forth.
  """
  if isinstance(x, Quantity):
    return Quantity(jnp.vander(x.value, N=N, increasing=increasing), dim=x.dim)
  elif isinstance(x, (jax.Array, np.ndarray)):
    return jnp.vander(x, N=N, increasing=increasing)
  else:
    raise ValueError(f'Unsupported type: {type(x)} for vander')
