#!/usr/bin/env python3
#
#  test_linear_regression.py
#
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
#  Based on Pyteomics (https://github.com/levitsky/pyteomics)
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
import string
from itertools import count
from typing import Tuple

# 3rd party
import numpy
import pytest

# this package
from mathematical import linear_regression

psms = list(zip(count(), string.ascii_uppercase + string.ascii_lowercase, numpy.arange(0.01, 0.062, 0.001)))


class Data:
	x = [1, 2, 3]
	y = [3, 5, 7]
	a = 2
	b = 1
	r = 1
	stderr = 0


def _test_linreg(result: Tuple[float, float, float, float]) -> None:
	a, b, r, stderr = result
	assert round(abs(a - Data.a), 7) == 0
	assert round(abs(b - Data.b), 7) == 0
	assert round(abs(r - Data.r), 7) == 0
	assert round(abs(stderr - Data.stderr), 7) == 0


def test_linear_regression_simple():
	result = linear_regression.linear_regression(Data.x, Data.y)
	_test_linreg(result)


def test_linear_regression_simple_vertical():
	result = linear_regression.linear_regression_vertical(Data.x, Data.y)
	_test_linreg(result)


def test_linear_regression_simple_perpendicular():
	result = linear_regression.linear_regression_perpendicular(Data.x, Data.y)
	_test_linreg(result)


def test_linear_regression_no_y_list():
	x = list(zip(Data.x, Data.y))
	result = linear_regression.linear_regression(x)  # type: ignore[arg-type]
	_test_linreg(result)


def test_linear_regression_no_y_list_vertical():
	x = list(zip(Data.x, Data.y))
	result = linear_regression.linear_regression_vertical(x)  # type: ignore[arg-type]
	_test_linreg(result)


def test_linear_regression_no_y_list_perpendicular():
	x = list(zip(Data.x, Data.y))
	result = linear_regression.linear_regression_perpendicular(x)  # type: ignore[arg-type]
	_test_linreg(result)


def test_linear_regression_no_y_arr():
	x = numpy.array(list(zip(Data.x, Data.y)))
	result = linear_regression.linear_regression(x)
	_test_linreg(result)


def test_linear_regression_no_y_arr_vertical():
	x = numpy.array(list(zip(Data.x, Data.y)))
	result = linear_regression.linear_regression_vertical(x)
	_test_linreg(result)


def test_linear_regression_no_y_arr_perpendicular():
	x = numpy.array(list(zip(Data.x, Data.y)))
	result = linear_regression.linear_regression_perpendicular(x)
	_test_linreg(result)


def test_linear_regression_shape_exception_vertical():
	with pytest.raises(TypeError):
		linear_regression.linear_regression_vertical(Data.x)


def test_linear_regression_shape_exception_perpendicular():
	with pytest.raises(TypeError):
		linear_regression.linear_regression_perpendicular(Data.x)
