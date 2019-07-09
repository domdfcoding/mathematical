#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
"""Utilities for Mathematical Operations"""
#
#  Copyright 2014-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
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


def magnitude(x):
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


def remove_zero(inputlist):
	"""
	Remove zero values from the given list
	Also removes False and None

	:param inputlist: list to remove zero values from
	:type inputlist: list

	:return: list without zero values
	:rtype: list
	"""
	
	import numpy as np
	inputlist = np.array(inputlist)
	return list(inputlist[np.nonzero(inputlist)])


def isint(num):  # Only works with floating point numbers
	"""
	Checks whether a float is an integer value

	:param num: value to check
	:type num: float

	:rtype: Boolean
	"""
	
	if num == int(num):
		return True
	else:
		return False


def RepresentsInt(s):
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


def rounders(val_to_round, round_format):
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


def strip_strings(ls):
	"""
	Remove strings from a list

	:param ls: the list to remove strings from
	:type ls: list

	:return: list without strings
	:rtype: list
	"""
	
	return [x for x in ls if not type(x) == str]


def strip_booleans(ls):
	"""
	Remove booleans from a list

	:param ls: the list to remove booleans from
	:type ls: list

	:return: list without booleans
	:rtype: list
	"""
	
	return [x for x in ls if not type(x) == bool]


def strip_nonetype(ls):
	"""
	Remove None from a list

	:param ls: the list to remove None from
	:type ls: list

	:return: list without None
	:rtype: list
	"""
	
	return [x for x in ls if x is not None]


def strip_none_bool_string(ls):
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


# The following functions copied from domdfcoding/Python_Modules

def gcd(a, b):
	"""
	Returns the GCD (HCF) of a and b using Euclid's Algorithm
	
	:param a:
	:param b:
	
	:return:
	"""

	while a != 0:
		a, b = b % a, a
	return b


def gcd2(numbers):
	"""
	Returns the GCD (HCF) of a list of numbers using Euclid's Algorithm
	
	:param numbers:
	
	:return:
	"""
	
	c = numbers[0]
	for i in range(1, (len(numbers))):
		c = gcd(c, numbers[i])
	return c


def lcm(numbers):
	"""
	Returns the LCM of a list of numbers using Euclid's Algorithm
	:param numbers:
	
	:return:
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


def hcf(a, b):
	"""
	
	:param a:
	:param b:
	
	:return:
	"""
	
	gcd(a, b)


def hcf2(numbers):
	"""
	
	:param numbers:
	
	:return:
	"""
	
	gcd2(numbers)


def modInverse(a, m):
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


