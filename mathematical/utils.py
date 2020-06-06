#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
"""Utilities for Mathematical Operations"""
#
#  Copyright 2014-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import decimal
import math
from decimal import Decimal
from operator import eq, ge, gt, le, lt, ne
from typing import Any, List, Optional, Sequence, Union

# 3rd party
import numpy  # type: ignore


def intdiv(p: float, q: float) -> int:
	"""
	Integer divsions which rounds toward zero

	Examples
	--------
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
	Examples
	--------
	>>> roman(4)
	'IV'
	>>> roman(17)
	'XVII'
	"""

	tokens = 'M CM D CD C XC L XL X IX V IV I'.split()
	values = 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
	result = ''
	for t, v in zip(tokens, values):
		cnt = num // v
		result += t * cnt
		num -= v * cnt
	return result


def magnitude(x: float) -> int:
	"""
	Determine the magnitude of the given value

	:param x: Numerical value to find the magnitude of

	:return: magnitude
	:rtype: int
	"""

	from math import log10
	if x > 0.0:
		return int(log10(x))
	else:
		return 0


# def _mag(num):
# 	return int(math.floor(math.log10(abs(num))))


def remove_zero(inputlist: Sequence[Union[float, bool, None]]) -> List[float]:
	"""
	Remove zero values from the given list
	Also removes False and None

	:param inputlist: list to remove zero values from
	:type inputlist: list

	:return: list without zero values
	:rtype: list
	"""

	inputlist = numpy.array(inputlist)
	return list(inputlist[numpy.nonzero(inputlist)])


def isint(num: float) -> bool:  # Only works with floating point numbers
	"""
	Checks whether a float is an integer value

	:param num: value to check
	:type num: float

	:rtype: Boolean
	"""

	return num == int(num)


def RepresentsInt(s: Any) -> bool:
	"""
	Checks whether a value can be converted to int

	:param s: value to check

	:rtype: Boolean
	"""
	try:
		int(s)
		return True
	except (ValueError, TypeError) as e:
		return False


def rounders(val_to_round: Union[str, float, Decimal], round_format: str) -> Decimal:
	"""
	Round a value to the specified number format, e.g. "0.000" for three decimal places

	:param val_to_round: The value to round
	:param round_format: The rounding format
	:type round_format: str

	:return: the rounded value
	:rtype: decimal.Decimal
	"""

	from decimal import Decimal, ROUND_HALF_UP
	return Decimal(Decimal(val_to_round).quantize(Decimal(str(round_format)), rounding=ROUND_HALF_UP))


def strip_strings(ls: Sequence[Any]) -> List:
	"""
	Remove strings from a list

	:param ls: the list to remove strings from
	:type ls: list

	:return: list without strings
	:rtype: list
	"""

	return [x for x in ls if not isinstance(x, str)]


def strip_booleans(ls: Sequence[Any]) -> List:
	"""
	Remove booleans from a list

	:param ls: the list to remove booleans from
	:type ls: list

	:return: list without booleans
	:rtype: list
	"""

	return [x for x in ls if not isinstance(x, bool)]


def strip_nonetype(ls: Sequence[Any]) -> List:
	"""
	Remove None from a list

	:param ls: the list to remove None from
	:type ls: list

	:return: list without None
	:rtype: list
	"""

	return [x for x in ls if x is not None]


def strip_none_bool_string(ls: Sequence[Any]) -> List:
	"""
	Remove None, Boolean and strings from a list

	:param ls: the list to remove values from
	:type ls: list

	:rtype: list
	"""

	ls = strip_nonetype(ls)
	ls = strip_booleans(ls)
	ls = strip_strings(ls)
	return ls


def gcd(a: int, b: int) -> int:
	"""
	Returns the GCD (HCF) of a and b using Euclid's Algorithm

	:param a:
	:param b:

	:return:
	"""

	# while a != 0:
	# 	a, b = b % a, a
	# return b
	return math.gcd(a, b)


def gcd_array(array) -> float:
	"""
	Returns the GCD for an array of numbers using Euclid's Algorithm

	Based on https://www.geeksforgeeks.org/python-program-for-gcd-of-more-than-two-or-array-numbers/

	:param array:
	:type array:
	:return:
	:rtype: float
	"""

	a = array[0]
	b = array[1]
	x = math.gcd(a, b)

	for i in range(2, len(array)):
		x = math.gcd(x, array[i])

	return x


def gcd2(numbers: int) -> int:
	"""
	Returns the GCD (HCF) of a list of numbers using Euclid's Algorithm

	:param numbers:

	:return:float
	"""

	c = numbers[0]
	for i in range(1, (len(numbers))):
		c = gcd(c, numbers[i])
	return c


def lcm(numbers: Sequence[float]) -> float:
	"""
	Returns the LCM of a list of numbers using Euclid's Algorithm
	:param numbers:

	:return: float
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


def hcf(a: int, b: int) -> int:
	"""

	:param a:
	:param b:

	:return:int
	"""

	gcd(a, b)


def hcf2(numbers: int) -> int:
	"""

	:param numbers:

	:return:int
	"""

	gcd2(numbers)


def modInverse(a: int, m: int) -> Optional[float]:
	"""
	Returns the modular inverse of a % m, which is the number x such that a*x % m = 1
	:param a:
	:param m:

	:return:
	"""

	if gcd(a, m) != 1:
		return None  # No mod inverse exists if a & m aren't relatively prime

	# Calculation using the Extended Euclidean Algorithm
	u1, u2, u3 = 1, 0, a
	v1, v2, v3 = 0, 1, m
	while v3 != 0:
		q = u3 // v3  # // forces integer division in Python 3
		v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
	return u1 % m


equiv_operators = dict(zip('< <= == != >= >'.split(), (lt, le, eq, ne, ge, gt)))

_precalc_fact = numpy.log([math.factorial(n) for n in range(20)])


def log_factorial(x: float) -> float:
	x = numpy.array(x)
	pf = _precalc_fact
	m = (x >= pf.size)
	out = numpy.empty(x.shape)
	out[~m] = pf[x[~m].astype(int)]
	x = x[m]
	out[m] = x * numpy.log(x) - x + 0.5 * numpy.log(2 * numpy.pi * x)
	return out


def _log_pi_r(d: float, k: float, p: float = 0.5) -> float:
	return k * math.log(p) + log_factorial(k + d) - log_factorial(k) - log_factorial(d)


def _log_pi(d: float, k: float, p: float = 0.5) -> float:
	return _log_pi_r(d, k, p) + (d + 1) * math.log(1 - p)


def _expectation(d: float, T: float, p: float = 0.5):
	if T is None:
		return d + 1
	T = numpy.array(T, dtype=int)
	m = numpy.arange(T.max() + 1, dtype=int)
	pi = numpy.exp(_log_pi(d, m, p))
	return ((m * pi).cumsum() / pi.cumsum())[T]


def _confidence_value(conf: float, d: float, T: float, p: float = 0.5):
	if T is not None:
		T = numpy.array(T, dtype=int)
		m = numpy.arange(T.max() + 1, dtype=int)
	else:
		m = numpy.arange(max(50 * d, 10000))
	log_pi = _log_pi(d, m, p)
	pics = numpy.exp(log_pi).cumsum()
	return numpy.searchsorted(pics, conf * (pics[T] if T is not None else 1))
