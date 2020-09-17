#!/usr/bin/env python
#
#  outliers.py
"""
Outlier detection functions.
"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  mad_outliers based on https://eurekastatistics.com/using-the-median-absolute-deviation-to-find-outliers/
# 		Copyright 2013 Peter Rosenmai
#
#  quartile_outliers based on http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
# 		Copyright 2012 NIST
#
#  spss_outliers based on http://www.unige.ch/ses/sococ/cl/spss/concepts/outliers.html
# 		Copyright 2018 Eugene Horber, U. of Geneva
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

# stdlib
from typing import List, Sequence, Tuple

# 3rd party
import numpy  # type: ignore

# this package
from . import stats, utils

__all__ = ["mad_outliers", "two_stdev", "stdev_outlier", "quartile_outliers", "spss_outliers"]


def mad_outliers(
		dataset: Sequence[float],
		strip_zero: bool = True,
		threshold: int = 3,
		) -> Tuple[List[float], List[float]]:
	"""
	Identifies outlier values using the Median Absolute Deviation.

	:param dataset:
	:param strip_zero:
	:param threshold: The multiple of MAD above which values are considered to be outliers

		Leys et al. (2013) make the following recommendations:

		1. In univariate statistics, the Median Absolute Deviation is the most robust
		   dispersion/scale measure in presence of outliers, and hence we strongly
		   recommend the median plus or minus 2.5 times the MAD method for outlier
		   detection.
		2. The threshold should be justified and the justification should clearly
		   state that other concerns than cherry-picking degrees of freedom guided
		   the selection. By default, we suggest a threshold of 2.5 as a
		   reasonable choice.
		3. We encourage researchers to report information about outliers, namely:
		   the number of outliers removed and their value (or at least the distance
		   between outliers and the selected threshold)

		.. seealso:: https://dipot.ulb.ac.be/dspace/bitstream/2013/139499/1/Leys_MAD_final-libre.pdf

	:returns: A list of the outlier values, and the remaining data points.
	"""

	dataset = utils.strip_none_bool_string(dataset)

	if strip_zero:
		dataset = utils.remove_zero(dataset)

	if len(dataset) < 2:
		return [], dataset

	abs_mad = stats.absolute_deviation_from_median(dataset)

	outliers = []
	data_exc_outliers = []

	for mad_value, value in zip(abs_mad, dataset):
		if mad_value > threshold or -threshold > mad_value:
			outliers.append(value)
		else:
			data_exc_outliers.append(value)

	return outliers, data_exc_outliers


def two_stdev(
		dataset: Sequence[float],
		strip_zero: bool = True,
		) -> Tuple[List[float], List[float]]:
	"""
	Identifies outlier values that are greater than ``2×`` stdev from the mean.

	:param dataset:
	:param strip_zero:

	:returns: A list of the outlier values, and the remaining data points.
	"""

	return stdev_outlier(dataset, strip_zero=strip_zero)


def stdev_outlier(
		dataset: Sequence[float],
		strip_zero: bool = True,
		rng: int = 2,
		) -> Tuple[List[float], List[float]]:
	"""
	Identifies outlier values that are greater than ``rng × stdev`` from mean.

	:param dataset:
	:param strip_zero:
	:param rng:

	:returns: A list of the outlier values, and the remaining data points.
	"""

	dataset = utils.strip_none_bool_string(dataset)

	if strip_zero:
		dataset = utils.remove_zero(dataset)

	if len(dataset) < 2:
		return [], dataset

	data_mean = numpy.mean(dataset)
	data_stdev = numpy.std(dataset, ddof=1)

	outliers = []
	data_exc_outliers = []

	for value in dataset:
		if value > (data_mean + (rng * data_stdev)) or -(data_mean + (rng * data_stdev)) > value:
			outliers.append(value)
		else:
			data_exc_outliers.append(value)

	return outliers, data_exc_outliers


def quartile_outliers(
		dataset: Sequence[float],
		strip_zero: bool = True,
		) -> Tuple[List[float], List[float]]:
	"""
	Identifies outlier values that are more than ``3×`` the inter-quartile range
	from the upper or lower quartile.

	:param dataset:
	:param strip_zero:

	:returns: A list of the outlier values, and the remaining data points.
	"""  # noqa D400

	dataset = utils.strip_none_bool_string(dataset)

	if strip_zero:
		dataset = utils.remove_zero(dataset)

	if len(dataset) < 2:
		return [], dataset

	q1 = numpy.percentile(dataset, 25)
	q3 = numpy.percentile(dataset, 75)
	iq = q3 - q1
	upper_outer_fence = q3 + (3 * iq)
	lower_outer_fence = q3 - (3 * iq)

	outliers = []
	data_exc_outliers = []

	for value in dataset:
		# print(value)
		if not lower_outer_fence < value < upper_outer_fence:
			# dataset.remove(value)
			outliers.append(value)
		else:
			data_exc_outliers.append(value)

	# return outliers, dataset
	return outliers, data_exc_outliers


def spss_outliers(
		dataset: Sequence[float],
		strip_zero: bool = True,
		mode: str = "all",
		) -> Tuple[List[float], List[float], List[float]]:
	"""
	Identifies outlier values using the IBM SPSS method.

	Outlier values are more than ``1.5 × IQR`` from ``Q1`` or ``Q3``.

	"Extreme values" are more than ``3 × IQR`` from ``Q1`` or ``Q3``.

	:param dataset:
	:param mode: str

	:returns: A list of extreme outliers, a list of other outliers, and the remaining data points.
	"""

	if len(dataset) < 2:
		raise ValueError("Dataset too small")

	if list(set(dataset)) in [None, 0.0, '', 0]:
		return [], [], list(dataset)

	for i in range(2):
		dataset = [x for x in dataset if x is not None]
		for val in dataset:
			if val in ['', 0.0, 0]:
				dataset.remove(val)

	if len(dataset) == 0:
		return [], [], list(dataset)
	elif dataset == [None]:
		return [], [], list(dataset)

	q1 = numpy.percentile(dataset, 25)
	# 	print(q1)
	q3 = numpy.percentile(dataset, 75)
	# 	print(q3)
	iq = q3 - q1
	# 	print(iq)

	upper_outlier_fence = q3 + (1.5 * iq)
	lower_outlier_fence = q3 - (1.5 * iq)

	upper_extreme_fence = q3 + (3 * iq)
	lower_extreme_fence = q3 - (3 * iq)

	outliers = []
	extremes = []
	data_exc_outliers = []

	for value in dataset:
		if not lower_extreme_fence < value < upper_extreme_fence:
			extremes.append(value)
		elif not lower_outlier_fence < value < upper_outlier_fence:
			outliers.append(value)
		else:
			data_exc_outliers.append(value)

	return extremes, outliers, data_exc_outliers


if __name__ == "__main__":
	# my_data = [70,72,74,76,80,114]
	my_data = [1, 2, 3, 3, 4, 4, 4, 5, 5.5, 6, 6, 6.5, 7, 7, 7.5, 8, 9, 12, 52, 90]
	# print("two stdev")
	# print(two_stdev(my_data))
	# print(numpy.mean(two_stdev(my_data)[1]))
	# print(numpy.median(two_stdev(my_data)[1]))
	# print("mad")
	# print(mad_outliers(my_data))
	# print(numpy.mean(mad_outliers(my_data)[1]))
	# print(numpy.median(mad_outliers(my_data)[1]))
	# print("quartile")
	# print(quartile_outliers(my_data))
	# print(numpy.mean(quartile_outliers(my_data)[1]))
	# print(numpy.median(quartile_outliers(my_data)[1]))

	print(spss_outliers(my_data))
