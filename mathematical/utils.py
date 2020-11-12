#!/usr/bin/env python
#
#  utils.py
"""
Utilities for mathematical operations.
"""
#
#  Copyright © 2014-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  intdiv, roman, and equiv_operators based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  gcd_array based on
#     https://www.geeksforgeeks.org/python-program-for-gcd-of-more-than-two-or-array-numbers/
#
#  _precalc_fact, log_factorial, _log_pi_r, _log_pi, _expectation,
#  and _confidence_value based on Pyteomics (https://github.com/levitsky/pyteomics)
#  |  Copyright (c) 2011-2015, Anton Goloborodko & Lev Levitsky
#  |  Licensed under the Apache License, Version 2.0 (the "License");
#  |  you may not use this file except in compliance with the License.
#  |  You may obtain a copy of the License at
#  |
#  |    http://www.apache.org/licenses/LICENSE-2.0
#  |
#  |  Unless required by applicable law or agreed to in writing, software
#  |  distributed under the License is distributed on an "AS IS" BASIS,
#  |  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  |  See the License for the specific language governing permissions and
#  |  limitations under the License.
#  |
#  |  See also:
#  |  Goloborodko, A.A.; Levitsky, L.I.; Ivanov, M.V.; and Gorshkov, M.V. (2013)
#  |  "Pyteomics - a Python Framework for Exploratory Data Analysis and Rapid Software
#  |  Prototyping in Proteomics", Journal of The American Society for Mass Spectrometry,
#  |  24(2), 301–304. DOI: `10.1007/s13361-012-0516-6 <http://dx.doi.org/10.1007/s13361-012-0516-6>`_
#  |
#  |  Levitsky, L.I.; Klein, J.; Ivanov, M.V.; and Gorshkov, M.V. (2018)
#  |  "Pyteomics 4.0: five years of development of a Python proteomics framework",
#  |  Journal of Proteome Research.
#  |  DOI: `10.1021/acs.jproteome.8b00717 <http://dx.doi.org/10.1021/acs.jproteome.8b00717>`_
#

# stdlib
import math
from decimal import ROUND_HALF_UP, Decimal
from math import log10
from operator import eq, ge, gt, le, lt, ne
from typing import Any, Iterator, List, Optional, Sequence, Union, overload

# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.typing import PathLike
from pandas import DataFrame

pandas.DataFrame.__module__ = "Pandas"

__all__ = [
		"intdiv",
		"roman",
		"magnitude",
		"remove_zero",
		"isint",
		"represents_int",
		"rounders",
		"strip_strings",
		"strip_booleans",
		"strip_nonetype",
		"nanmean",
		"nanstd",
		"nanrsd",
		"strip_none_bool_string",
		"gcd",
		"gcd_array",
		"gcd2",
		"lcm",
		"hcf",
		"hcf2",
		"mod_inverse",
		"log_factorial",
		"equiv_operators",
		"FRange",
		"concatenate_csv",
		]


def intdiv(p: float, q: float) -> int:
	"""
	Integer divsions which rounds toward zero.

	**Examples**
	>>> intdiv(3, 2)
	1
	>>> intdiv(-3, 2)
	-1
	>>> -3 // 2
	-2
	"""

	r = p // q

	if r < 0 and q * r != p:
		r += 1

	return int(r)


def roman(num: float) -> str:
	"""
	Retuns the Roman numeral represtation of the given value.

	**Examples:**

	.. code-block::

		>>> roman(4)
		'IV'
		>>> roman(17)
		'XVII'
	"""

	tokens = "M CM D CD C XC L XL X IX V IV I".split()
	values = 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
	result = ''

	for t, v in zip(tokens, values):
		cnt = int(num // v)
		result += t * cnt
		num -= v * cnt

	return result


def magnitude(x: float) -> int:
	"""
	Returns the magnitude of the given value.

	:param x: Numerical value to find the magnitude of.

	.. versionchanged:: 0.2.0

		Now returns the absolute magnitude of negative numbers.
	"""

	if x > 0.0:
		return int(log10(x))
	elif x < 0.0:
		return int(log10(abs(x)))
	else:
		return 0


def remove_zero(inputlist: Sequence[Union[float, bool, None]]) -> List[float]:
	"""
	Remove zero values from the given list.

	Also removes :py:obj:`False` and :py:obj:`None`.

	:param inputlist: list to remove zero values from
	"""

	inputlist = numpy.array(inputlist)
	return list(inputlist[numpy.nonzero(inputlist)])


def isint(num: float) -> bool:
	"""
	Checks whether a float is an integer value.

	.. note:: This function only works with floating-point numbers

	:param num: value to check

	:rtype: bool
	"""

	return num == int(num)


def represents_int(s: Any) -> bool:
	"""
	Checks whether a value can be converted to an :class:`int`.

	:param s: value to check

	:rtype: bool
	"""

	try:
		int(s)
		return True
	except (ValueError, TypeError):
		return False


RepresentsInt = represents_int


def rounders(val_to_round: Union[str, float, Decimal], round_format: str) -> Decimal:
	"""
	Round a value to the specified number format, e.g. ``"0.000"`` for three decimal places.

	:param val_to_round: The value to round
	:param round_format: The rounding format
	"""

	return Decimal(Decimal(val_to_round).quantize(Decimal(str(round_format)), rounding=ROUND_HALF_UP))


def strip_strings(ls: Sequence[Any]) -> List:
	"""
	Remove strings from a list.

	:param ls: the list to remove strings from.

	:return: The list without strings.
	"""

	return [x for x in ls if not isinstance(x, str)]


def strip_booleans(ls: Sequence[Any]) -> List:
	"""
	Remove booleans from a list.

	:param ls: the list to remove booleans from.

	:return: The list without boolean values.
	"""

	return [x for x in ls if not isinstance(x, bool)]


def strip_nonetype(ls: Sequence[Any]) -> List:
	"""
	Remove None from a list.

	:param ls: the list to remove None from.

	:return: The list without :py:obj:`None` values.
	"""

	return [x for x in ls if x is not None]


def nanmean(ls: Sequence[Any], dtype=float) -> float:
	"""
	Returns the mean of the given sequence, ignoring :py:obj:`None` and ``numpy.nan`` values etc.

	Similar to numpy.nanmean except it handles :py:obj:`None`.

	:param ls:
	:param dtype:
	"""

	return float(numpy.nanmean(numpy.array(ls, dtype=dtype)))


def nanstd(ls: Sequence[Any], dtype=float) -> float:
	"""
	Returns the standard deviation of the given sequence, ignoring :py:obj:`None` and ``numpy.nan`` values etc.

	Similar to numpy.nanstd except it handles :py:obj:`None`.

	:param ls:
	:param dtype:
	"""

	return float(numpy.nanstd(numpy.array(ls, dtype=dtype)))


def nanrsd(ls: Sequence[Any], dtype=float) -> float:
	"""
	Returns the relative standard deviation of the given sequence, ignoring :py:obj:`None` and ``numpy.nan`` values etc.

	:param ls:
	:param dtype:
	"""

	mean = nanmean(ls, dtype=dtype)
	std = nanstd(ls, dtype=dtype)

	return float(std / abs(mean))


def strip_none_bool_string(ls: Sequence[Any]) -> List:
	"""
	Remove :py:obj:`None`, boolean and string values from a list.

	:param ls: The list to remove values from.
	"""

	ls = strip_nonetype(ls)
	ls = strip_booleans(ls)
	ls = strip_strings(ls)
	return ls


def gcd(a: int, b: int) -> int:
	"""
	Returns the GCD (HCF) of ``a`` and ``b`` using Euclid's Algorithm.

	:param a:
	:param b:
	"""

	# while a != 0:
	# 	a, b = b % a, a
	# return b

	return math.gcd(a, b)


def gcd_array(array) -> float:
	"""
	Returns the GCD for an array of numbers using Euclid's Algorithm.

	Based on https://www.geeksforgeeks.org/python-program-for-gcd-of-more-than-two-or-array-numbers/

	:param array:
	"""

	a = array[0]
	b = array[1]
	x = math.gcd(a, b)

	for i in range(2, len(array)):
		x = math.gcd(x, array[i])

	return x


def gcd2(numbers: Sequence[int]) -> int:
	"""
	Returns the GCD (HCF) of a list of numbers using Euclid's Algorithm.

	:param numbers:
	"""

	c = numbers[0]

	for i in range(1, (len(numbers))):
		c = gcd(c, numbers[i])

	return c


def lcm(numbers: Sequence[int]) -> float:
	"""
	Returns the LCM of a list of numbers using Euclid's Algorithm.

	:param numbers:
	"""

	product = numbers[0]

	for i in range(1, len(numbers)):
		product = product * numbers[i]

	gcd = gcd2(numbers)
	lcm = product / gcd

	if product % gcd == 0:
		return lcm
	else:
		return product


hcf = gcd

hcf2 = gcd2


def mod_inverse(a: int, m: int) -> Optional[float]:
	"""
	Returns the modular inverse of ``a % m``,
	which is the number ``x`` such that ``a × x % m = 1``.

	:param a:
	:param m:
	"""  # noqa D400

	if gcd(a, m) != 1:
		return None  # No mod inverse exists if a & m aren't relatively prime

	# Calculation using the Extended Euclidean Algorithm
	u1, u2, u3 = 1, 0, a
	v1, v2, v3 = 0, 1, m

	while v3 != 0:
		q = u3 // v3  # // forces integer division in Python 3
		v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

	return u1 % m


modInverse = mod_inverse

equiv_operators = dict(zip("< <= == != >= >".split(), (lt, le, eq, ne, ge, gt)))

_precalc_fact = numpy.log([math.factorial(n) for n in range(20)])


def log_factorial(x: float) -> float:
	"""

	:param x:
	"""

	arr = numpy.array(x)
	m: bool = (arr >= _precalc_fact.size)
	out = numpy.empty(arr.shape)

	out[~m] = _precalc_fact[arr[~m].astype(int)]
	arr = arr[m]
	out[m] = arr * numpy.log(arr) - arr + 0.5 * numpy.log(2 * numpy.pi * arr)

	return float(out)


def _log_pi_r(d: float, k: float, p: float = 0.5) -> float:
	return k * math.log(p) + log_factorial(k + d) - log_factorial(k) - log_factorial(d)


def _log_pi(d: float, k: float, p: float = 0.5) -> float:
	return _log_pi_r(d, k, p) + (d + 1) * math.log(1 - p)


@prettify_docstrings
class FRange(Sequence[float]):
	"""
	Returns a range of floating-point numbers.

	The arguments to the range constructor may be integers or floats.

	:param start:
	:param stop:
	:param step:

	:raises ValueError: If step is zero, or if any value is larger than 1×10 :superscript:`14`.

	.. versionadded:: 0.2.0
	"""

	#: The value of the ``start`` parameter (or ``0.0`` if the parameter was not supplied)
	start: float

	#: The value of the ``stop`` parameter
	stop: float

	#: The value of the ``step`` parameter (or ``1.0`` if the parameter was not supplied)
	step: float

	_init = False

	def __setattr__(self, key, value):
		if self._init:
			raise AttributeError("Could not set attribute")
		else:
			super().__setattr__(key, value)

	def __delattr__(self, key):
		if self._init:
			raise AttributeError("Could not delete attribute")
		else:
			super().__delattr__(key)

	@overload
	def __init__(self, stop: float) -> None:
		...  # pragma: no cover

	@overload
	def __init__(self, start: float, stop: float, step: float = ...) -> None:
		...  # pragma: no cover

	def __init__(self, start=None, stop=None, step=1.0) -> None:  # type: ignore
		if start is not None and stop is None:
			self.stop = float(start)
			self.start = 0.0
		elif start is not None and stop is not None:
			self.start = float(start)
			self.stop = float(stop)
		else:
			raise TypeError("Invalid argument types.")

		if step == 0.0:
			raise ValueError("'step' argument must not be zero")
		else:
			self.step = float(step)

		if magnitude(self.start) > 14:
			raise ValueError(f"Value {self.start} too large for 'start'")
		if magnitude(self.stop) > 14:
			raise ValueError(f"Value {self.stop} too large for 'stop'")
		if magnitude(self.step) > 14:
			raise ValueError(f"Value {self.step} too large for 'step'")

		self._init = True

	def count(self, value: float) -> int:
		"""
		Returns ``1`` if the value is within the range, ``0`` otherwise.

		:param value:
		"""

		if value in self:
			return 1
		else:
			return 0

	def index(self, value: float) -> int:  # type: ignore
		"""
		Returns the index of ``value`` in the range.

		:param value:

		:raises ValueError: if the value is not in the range.
		"""

		if value not in self:
			raise ValueError(f"{value} is not in range")
		else:
			return int((value - self.start) / self.step)

	def __len__(self) -> int:
		"""
		Returns the number of values in the range.
		"""

		if self.stop <= self.start and self.step > 0:
			return 0
		elif self.stop >= self.start and self.step < 0:
			return 0
		else:
			return math.ceil((self.stop - self.start) / self.step)

	def __contains__(self, o: object) -> bool:
		"""
		Returns whether ``o`` is in the range.

		:param o:
		"""

		if isinstance(o, (int, float)):
			if self.step > 0:
				return (self.start <= o < self.stop) and not ((o - self.start) % self.step)
			elif self.step < 0:
				return (self.start >= o > self.stop) and not ((o - self.start) % self.step)
		return False

	def __iter__(self) -> Iterator[float]:
		"""
		Iterates over values in the range.
		"""

		count = 0

		while True:
			value = float(self.start + count * self.step)

			if self.step > 0 and value >= self.stop:
				break
			elif self.step < 0 and value <= self.stop:
				break
			else:
				yield value

			count += 1

	@overload
	def __getitem__(self, i: int) -> int:
		...

	@overload
	def __getitem__(self, s: slice) -> "FRange":
		...

	def __getitem__(self, item):
		"""
		Returns the value in the range at index ``item``.

		:param item:
		"""

		if isinstance(item, int) and item >= 0:
			value = self.start + (item * self.step)
			if value >= self.stop:
				raise IndexError("FRange object index out of range")
			else:
				return value
		elif isinstance(item, int):
			value = self.stop - (item * self.step)
			if value < self.start:
				raise IndexError("FRange object index out of range")
			else:
				return value
		# elif isinstance(item, slice):
		# 	step = item.step or 1
		# 	start_idx = item.start or 0
		#
		# 	if start_idx > len(self):
		# 		start = self.stop
		# 	else:
		# 		start = self[start_idx]
		#
		# 	if self.stop - (item.stop * self.step) < self.start:
		# 		stop = self.stop
		# 	else:
		# 		stop = self[item.stop]
		#
		# 	return self.__class__(start, stop, step)
		else:
			raise NotImplementedError(f"Unsupported type for __getitem__: {type(item)}")

	def __repr__(self) -> str:
		if self.step != 1.0:
			return f"FRange({self.start}, {self.stop}, {self.step})"
		else:
			return f"FRange({self.start}, {self.stop})"

	def __reversed__(self) -> Iterator[float]:
		"""
		Returns :func:`reversed(self) <reversed>`.
		"""

		# Special case where start == stop
		if self.start == self.stop:
			return iter(FRange(self.start, self.stop, -self.step))

		# difference between last value and self.stop
		remainder = ((self.stop - self.start) % self.step) or self.step

		return iter(FRange(
				start=(self.stop - remainder),
				stop=(self.start - self.step),
				step=-self.step,
				))

	def __eq__(self, other) -> bool:
		if isinstance(other, (range, FRange)):
			# if self.stop < self.start and self.step > 0:
			# 	self_stop = self.start
			# elif self.stop > self.start and self.step < 0:
			# 	self_stop = self.start
			# else:
			# 	self_stop = self.stop
			#
			# # difference between last value and self.stop
			# remainder = ((self_stop - self.start) % self.step)
			#
			# if self_stop == self.start:
			# 	self_step = 1
			# elif remainder:
			# 	self_step = 1
			# elif self_stop - self.step == self.start:
			# 	self_step = 1
			# else:
			# 	self_step = self.step
			#
			# if other.stop < other.start and other.step > 0:
			# 	other_stop = other.start
			# elif other.stop > other.start and other.step < 0:
			# 	other_stop = other.start
			# else:
			# 	other_stop = other.stop
			#
			# # difference between last value and other.stop
			# remainder = ((other_stop - other.start) % other.step)
			#
			# if other_stop == other.start:
			# 	other_step = 1
			# elif remainder:
			# 	other_step = 1
			# elif other_stop - other.step == other.start:
			# 	other_step = 1
			# else:
			# 	other_step = other.step
			#
			# if self.start == self_stop and other.start == other_stop and self_step == other_step:
			# 	return True
			# elif self_stop == other_stop and self.start == other.start and self_step == other_step:
			# 	return True
			# else:
			# 	return False

			# for left, right in zip_longest(self, other):
			# 	if left != right:
			# 		return False
			# return True
			return tuple(self) == tuple(other)

		else:
			return False

	def __hash__(self):
		return hash(tuple(self))


def concatenate_csv(*files: PathLike, outfile: Optional[PathLike] = None) -> DataFrame:
	r"""
	Concatenate multiple CSV files together and return a :class:`pandas.DataFrame` representing the output.

	:param \*files: The files to concatenate.
	:param outfile: The file to save the output as. If :py:obj:`None` no file will be saved.

	:return: A :class:`pandas.DataFrame` containing the concatenated CSV data

	.. versionadded:: 0.3.0
	"""

	data_frames = []

	for csv_file in files:
		# Read CSV file to data frame
		results_df = pandas.read_csv(csv_file, header=0, index_col=False, dtype=str)

		data_frames.append(results_df)

	concat_df = pandas.concat(data_frames)

	if outfile is not None:
		concat_df.to_csv(outfile, index=False)

	return concat_df
