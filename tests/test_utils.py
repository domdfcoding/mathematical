# -*- coding: utf-8 -*-
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

import decimal
import numpy

from mathematical import utils

data = [1, 2, 3, 4, 5, 0, "abc", False, None, numpy.nan]


def test_roman():
	assert utils.roman(4) == 'IV'
	assert utils.roman(20) == 'XX'
	assert utils.roman(94) == 'XCIV'
	assert utils.roman(501) == 'DI'


def test_magnitude():
	assert isinstance(utils.magnitude(1234), int)
	assert utils.magnitude(1234) == 3


def test_remove_zero():
	assert isinstance(utils.remove_zero(data), list)
	assert utils.remove_zero(data) == [1, 2, 3, 4, 5, "abc", numpy.nan]


def test_isint():
	assert isinstance(utils.isint(1), bool)
	assert isinstance(utils.isint(1.0), bool)
	assert utils.isint(1)
	assert utils.isint(1.0)


def test_RepresentsInt():
	assert isinstance(utils.RepresentsInt(1), bool)
	assert isinstance(utils.RepresentsInt(1.0), bool)
	assert isinstance(utils.RepresentsInt("1"), bool)
	assert utils.RepresentsInt(1)
	assert utils.RepresentsInt(1.0)
	assert utils.RepresentsInt("1")


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
