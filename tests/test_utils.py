# !/usr/bin/env python3
#
#  test_utils.py
"""

Test functions in utils.py

"""
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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
#  test_roman from ChemPy (https://github.com/bjodah/chempy)
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

# stdlib
import decimal

# 3rd party
import numpy
import pytest

# this package
from mathematical import utils
from mathematical.utils import nanmean, nanrsd, nanstd, represents_int

data = [1, 2, 3, 4, 5, 0, "abc", False, None, numpy.nan]


def test_roman():
	assert utils.roman(4) == "IV"
	assert utils.roman(20) == "XX"
	assert utils.roman(94) == "XCIV"
	assert utils.roman(501) == "DI"


def test_magnitude():
	assert isinstance(utils.magnitude(1234), int)
	assert utils.magnitude(1234) == 3
	assert utils.magnitude(2**100) == 30
	assert utils.magnitude(10**100) == 100
	assert utils.magnitude(-2**100) == 30


def test_remove_zero():
	result = utils.remove_zero(data)  # type: ignore
	assert isinstance(result, list)
	assert result == [1, 2, 3, 4, 5, "abc", numpy.nan]


@pytest.mark.parametrize(
		"value", [1, 3, 5, 7, 9, 90, 900, 9000000, 1.0, 3.0, 5.0, 7.0, 9.0, 90.0, 900.0, 9000000.0]
		)
def test_isint(value):
	result = utils.isint(value)
	assert isinstance(result, bool)
	assert result


@pytest.mark.parametrize(
		"value",
		[
				1,
				3,
				5,
				7,
				9,
				90,
				900,
				9000000,
				'1',
				'3',
				'5',
				'7',
				'9',
				"90",
				"900",
				"9000000",
				1.0,
				3.0,
				5.0,
				7.0,
				9.0,
				90.0,
				900.0,
				9000000.0
				]
		)
def test_RepresentsInt(value):
	result = utils.represents_int(value)
	assert isinstance(result, bool)
	assert result


def test_rounders():
	assert isinstance(utils.rounders(1234.5678, "0.0"), decimal.Decimal)
	assert str(utils.rounders(1234.5678, "0.0")) == "1234.6"


def test_strip_strings():
	assert isinstance(utils.strip_strings(data), list)
	assert utils.strip_strings(data) == [1, 2, 3, 4, 5, 0, False, None, numpy.nan]


def test_strip_booleans():
	assert isinstance(utils.strip_booleans(data), list)
	assert utils.strip_booleans(data) == [1, 2, 3, 4, 5, 0, "abc", None, numpy.nan]


def test_strip_nonetype():
	assert isinstance(utils.strip_nonetype(data), list)
	assert utils.strip_nonetype(data) == [1, 2, 3, 4, 5, 0, "abc", False, numpy.nan]


def test_strip_none_bool_string():
	assert isinstance(utils.strip_none_bool_string(data), list)
	assert utils.strip_none_bool_string(data) == [1, 2, 3, 4, 5, 0, numpy.nan]


# TODO: gcd, gcd2, lcm, hcf, hcf2, modInverse


@pytest.mark.parametrize(
		"value, result",
		[
				('1', True),
				('5', True),
				("10", True),
				("25", True),
				("50", True),
				("100", True),
				("1.0", False),
				("5.5", False),
				("10e10", False),
				("4j", False),
				(1, True),
				(5, True),
				(10, True),
				(25, True),
				(50, True),
				(100, True),
				(1.0, True),
				(5.5, True),
				(10e10, True),
				(4j, False),
				("ABC", False),
				("abc", False),
				]
		)
def test_represents_int(value, result: bool):
	assert represents_int(value) is result


@pytest.mark.parametrize(
		"values, result",
		[
				([1, 2, 3, 4, 5], 3),
				([1, 2, 3, 4, 5, None], 3),
				([1, 2, 3, 4, 5, numpy.nan], 3),
				([1, 2, 3, 4, 5, numpy.nan, None], 3),
				([1, 3, 5, numpy.nan], 3),
				([1, 3, 5, None], 3),
				([1, 3, 5, numpy.nan, None], 3),
				]
		)
def test_nanmean(values, result):
	assert nanmean(values) == result


def test_nanmean_allnan():
	assert numpy.isnan(nanmean([numpy.nan, None, float("nan")]))


@pytest.mark.parametrize(
		"values, result",
		[
				([1, 2, 3, 4, 5], 1.4142135623730951),
				([1, 2, 3, 4, 5, None], 1.4142135623730951),
				([1, 2, 3, 4, 5, numpy.nan], 1.4142135623730951),
				([1, 2, 3, 4, 5, numpy.nan, None], 1.4142135623730951),
				([1, 3, 5, numpy.nan], 1.632993161855452),
				([1, 3, 5, None], 1.632993161855452),
				([1, 3, 5, numpy.nan, None], 1.632993161855452),
				]
		)
def test_nanstd(values, result):
	assert nanstd(values) == result


def test_nanstd_allnan():
	assert numpy.isnan(nanstd([numpy.nan, None, float("nan")]))


@pytest.mark.parametrize(
		"values, result",
		[
				([1, 2, 3, 4, 5], 0.47140452079103173),
				([1, 2, 3, 4, 5, None], 0.47140452079103173),
				([1, 2, 3, 4, 5, numpy.nan], 0.47140452079103173),
				([1, 2, 3, 4, 5, numpy.nan, None], 0.47140452079103173),
				([1, 3, 5, numpy.nan], 0.5443310539518174),
				([1, 3, 5, None], 0.5443310539518174),
				([1, 3, 5, numpy.nan, None], 0.5443310539518174),
				]
		)
def test_nanrstd(values, result):
	assert nanrsd(values) == result


def test_nanrstd_allnan():
	assert numpy.isnan(nanrsd([numpy.nan, None, float("nan")]))
