#!/usr/bin/env python3
#
#  linear_regression.py
"""
Functions for performing linear regression.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Optional, Sequence, Tuple, Union

# 3rd party
import numpy  # type: ignore

__all__ = ["linear_regression_vertical", "linear_regression_perpendicular", "ArrayLike_Float"]

#: Type hint for arguments that take either a sequence of floats or a numpy array.
ArrayLike_Float = Union[Sequence[float], numpy.ndarray]


def linear_regression_vertical(
		x: ArrayLike_Float,
		y: Optional[ArrayLike_Float] = None,
		a: Optional[float] = None,
		b: Optional[float] = None,
		) -> Tuple[float, float, float, float]:
	"""
	Calculate coefficients of a linear regression y = a * x + b.
	The fit minimizes *vertical* distances between the points and the line.

	:param x: 1-D array of floats
	:param y: 1-D array of floats
	:param a: If specified then the slope coefficient is fixed as this value
	:param b: If specified then the free term is fixed as this value

	If `y` is omitted, `x` must be a 2-D array of shape (N, 2).

	:return: (a, b, r, stderr), where
		a -- slope coefficient,
		b -- free term,
		r -- Pearson correlation coefficient,
		stderr -- standard deviation.
	"""

	x = numpy.array(x, copy=False)
	if y is not None:
		y = numpy.array(y, copy=False)
	else:
		if len(x.shape) != 2 or x.shape[-1] != 2:
			raise TypeError(f"If `y` is not given, x.shape should be (N, 2), given: {x.shape}")
		y = x[:, 1]
		x = x[:, 0]
	if a is not None and b is None:
		b = (y - a * x).mean()
	elif a is not None and b is not None:
		pass
	else:
		a, b = numpy.polyfit(x, y, 1)

	r = numpy.corrcoef(x, y)[0, 1]
	stderr = (y - a * x - b).std()

	return a, b, r, stderr  # type: ignore  # TODO


linear_regression = linear_regression_vertical


def linear_regression_perpendicular(
		x: ArrayLike_Float,
		y: Optional[ArrayLike_Float] = None,
		) -> Tuple[float, float, float, float]:
	"""
	Calculate coefficients of a linear regression y = a * x + b.
	The fit minimizes *perpendicular* distances between the points and the line.

	:param x: 1-D array of floats.
	:param y: 1-D array of floats.

	If `y` is omitted, `x` must be a 2-D array of shape (N, 2).

	:return: (a, b, r, stderr), where
		a -- slope coefficient,
		b -- free term,
		r -- Peason correlation coefficient,
		stderr -- standard deviation.
	"""

	x = numpy.array(x, copy=False)

	if y is not None:
		y = numpy.array(y, copy=False)
		data = numpy.hstack((x.reshape((-1, 1)), y.reshape((-1, 1))))
	else:
		if len(x.shape) != 2 or x.shape[-1] != 2:
			raise TypeError(f"If `y` is not given, x.shape should be (N, 2), given: {x.shape}")
		data = x

	mu = data.mean(axis=0)
	eigenvectors, eigenvalues, V = numpy.linalg.svd((data - mu).T, full_matrices=False)
	a = eigenvectors[0][1] / eigenvectors[0][0]
	xm, ym = data.mean(axis=0)
	b = ym - a * xm

	r = numpy.corrcoef(data[:, 0], data[:, 1])[0, 1]
	stderr = ((data[:, 1] - a * data[:, 0] - b) / numpy.sqrt(a**2 + 1)).std()

	return a, b, r, stderr
