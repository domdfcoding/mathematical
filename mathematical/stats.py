#!/usr/bin/env python
#
#  stats.py
"""
Functions for calculating statistics.
"""
#
#  Copyright © 2014-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  _contains_nan, median_absolute_deviation, absolute_deviation and
#  absolute_deviation_from_median adapted from SciPy
#  Copyright (c) 2001-2002 Enthought, Inc.  2003-2019, SciPy Developers
#  Available under the BSD License
#
#  pooled_sd, g_hedge and g_durlak_bias based on formulae from
#  https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/hedgeg.htm
#
#  interpret_d based on Sullivan, G. and Feinn, R. (2012). Using Effect Size—or
#  		Why the P Value Is Not Enough. Journal of Graduate Medical Education,
#  		4(3), pp.279-282.
# 	and https://www.psychometrica.de/effect_size.html#transform
#
#  d_cohen based on Cohen, J. (1988). Statistical power analysis for the
#  		behavioral sciences (2nd Edition). Hillsdale, NJ: Lawrence Erlbaum Associates
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

# stdlib
import warnings  # type: ignore
from typing import Callable, Optional, Sequence, Union

# 3rd party
import numpy  # type: ignore
from typing_extensions import Literal

# this package
from . import utils

__all__ = [
		"mean_none",
		"std_none",
		"median_none",
		"iqr_none",
		"percentile_none",
		"pooled_sd",
		"d_cohen",
		"g_hedge",
		"g_durlak_bias",
		"interpret_d",
		"median_absolute_deviation",
		"absolute_deviation",
		"absolute_deviation_from_median",
		"within1min"
		]

#: Type hint for allowed values for ``nan_values``.
NaNPolicies = Literal["propagate", "raise", "omit"]


def mean_none(dataset: Sequence[Union[float, bool, None]]) -> float:
	"""
	Calculate the mean, excluding NaN, strings, boolean values, and zeros.

	:param dataset: list to calculate mean from

	:return: mean
	"""

	dataset = utils.strip_none_bool_string(dataset)
	dataset = utils.remove_zero(dataset)

	return float(numpy.nanmean(dataset))


def std_none(dataset: Sequence[Union[float, bool, None]], ddof: int = 1) -> float:
	"""
	Calculate the standard deviation, excluding NaN, strings, boolean values, and zeros.

	:param dataset: list to calculate mean from.
	:param ddof: Means Delta Degrees of Freedom. The divisor used in calculations is ``N - ddof``,
		where ``N`` represents the number of elements.

	:return: standard deviation
	"""

	dataset = utils.strip_none_bool_string(dataset)
	dataset = utils.remove_zero(dataset)
	# print(dataset)

	return float(numpy.nanstd(dataset, ddof=ddof))


def median_none(dataset: Sequence[Union[float, bool, None]]) -> float:
	"""
	Calculate the median, excluding NaN, strings, boolean values, and zeros.

	:param dataset: list to calculate median from

	:return: standard deviation
	"""

	dataset = utils.strip_none_bool_string(dataset)
	dataset = utils.remove_zero(dataset)

	return float(numpy.nanmedian(dataset))


def iqr_none(dataset: Sequence[Union[float, bool, None]]) -> float:
	"""
	Calculate the interquartile range, excluding NaN, strings, boolean values, and zeros.

	:param dataset: A list to calculate iqr from.

	:return: The interquartile range.
	"""

	q1 = percentile_none(dataset, 25)
	q3 = percentile_none(dataset, 75)
	iq = q3 - q1

	return float(iq)


def percentile_none(dataset: Sequence[Union[float, bool, None]], percentage: float) -> float:
	"""
	Calculate the given percentile, excluding NaN, strings, boolean values, and zeros.

	:param dataset: Sequence to calculate the percentile from.
	:param percentage:

	:raises: :exc:`ValueError` if ``dataset`` contains fewer than two values

	:return: The interquartile range.
	"""

	dataset = utils.strip_none_bool_string(dataset)
	dataset = utils.remove_zero(dataset)
	dataset = [x for x in dataset if not numpy.isnan(x)]

	if len(dataset) < 2:
		raise ValueError("Dataset too small")

	return float(numpy.percentile(dataset, percentage))


def pooled_sd(sample1: Sequence[float], sample2: Sequence[float], weighted: bool = False) -> float:
	"""
	Returns the pooled standard deviation.

	:param sample1: datapoints for first sample
	:param sample2: datapoints for second sample
	:param weighted: True for weighted pooled SD

	.. seealso:: https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/hedgeg.htm
	"""

	sd1 = numpy.std(sample1)
	sd2 = numpy.std(sample2)
	n1 = len(sample1)
	n2 = len(sample2)

	if weighted:
		return numpy.sqrt((((n1 - 1) * (sd1**2)) + ((n2 - 1) * (sd2**2))) / (n1 + n2 - 2))
	else:
		return numpy.sqrt(((sd1**2) + (sd2**2)) / 2)


def d_cohen(
		sample1: Sequence[float],
		sample2: Sequence[float],
		which: Literal[1, 2] = 1,
		tail: int = 1,
		pooled: bool = False,
		) -> float:
	"""
	Calculates and returns Cohen's d-Statistic.

	.. seealso::

		Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd Edition).
		Hillsdale, NJ: Lawrence Erlbaum Associates

	:param sample1: datapoints for first sample
	:param sample2: datapoints for second sample
	:param which: Use the standard deviation of the first sample (``1``) or the second sample (``2``)
	:param tail:
	:param pooled:
	"""

	mean1 = numpy.mean(sample1)
	mean2 = numpy.mean(sample2)

	if which == 1:
		stdev = numpy.std(sample1)
	else:
		stdev = numpy.std(sample2)

	if pooled:
		stdev = pooled_sd(sample1, sample2)

	if tail == 2:
		return numpy.abs(mean1 - mean2) / stdev

	return (mean1 - mean2) / stdev


def g_hedge(sample1: Sequence[float], sample2: Sequence[float]) -> float:
	"""
	Calculates and returns Hedge's g-Statistic.

	Formula from https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/hedgeg.htm

	:param sample1: datapoints for first sample
	:param sample2: datapoints for second sample
	"""

	mean1 = numpy.mean(sample1)
	mean2 = numpy.mean(sample2)
	return (mean1 - mean2) / pooled_sd(sample1, sample2, True)


def g_durlak_bias(g: float, n: float) -> float:
	"""
	Application of Durlak's bias correction to the Hedge's g statistic.

	n = n1+n2

	:param g:
	:param n:

	.. seealso:: https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/hedgeg.htm
	"""

	Durlak = ((n - 3) / (n - 2.25)) * numpy.sqrt((n - 2) / n)
	return g * Durlak


def interpret_d(d_or_g: float) -> str:
	"""
	Interpret Cohen's d or Hedge's g values using Table 1
	from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3444174/

	:param d_or_g:
	:type d_or_g:
	"""  # noqa D400

	if 0.0 <= d_or_g < 0.2:
		return "No Effect"
	elif 0.2 <= d_or_g < 0.5:
		return "Small Effect"
	elif 0.5 <= d_or_g < 0.8:
		return "Intermediate Effect"
	elif 0.8 <= d_or_g:
		return "Large Effect"
	else:  # d_or_g < 0
		return f"{interpret_d(numpy.abs(d_or_g)).split(' ')[0]} Adverse Effect"


def _contains_nan(a, nan_policy: NaNPolicies = "propagate"):
	policies = ["propagate", "raise", "omit"]
	if nan_policy not in policies:
		raise ValueError("nan_policy must be one of {%s}" % ", ".join(f"'{s}'" for s in policies))
	try:
		# Calling numpy.sum to avoid creating a huge array into memory
		# e.g. numpy.isnan(a).any()
		with numpy.errstate(invalid="ignore"):
			contains_nan = numpy.isnan(numpy.sum(a))
	except TypeError:
		# This can happen when attempting to sum things which are not
		# numbers (e.g. as in the function `mode`). Try an alternative method:
		try:
			contains_nan = numpy.nan in set(a.ravel())
		except TypeError:
			# Don't know what to do. Fall back to omitting nan values and
			# issue a warning.
			contains_nan = False
			nan_policy = "omit"
			warnings.warn(
					"The input array could not be properly checked for nan "
					"values. nan values will be ignored.",
					RuntimeWarning
					)

	if contains_nan and nan_policy == "raise":
		raise ValueError("The input contains nan values")

	return contains_nan, nan_policy


def median_absolute_deviation(
		x,
		axis: Optional[int] = 0,
		center: Callable = numpy.median,
		scale: float = 1.4826,
		nan_policy: NaNPolicies = "propagate"
		) -> numpy.ndarray:
	"""
	Compute the median absolute deviation of the data along the given axis.
	The median absolute deviation (MAD, [1]_) computes the median over the
	absolute deviations from the median. It is a measure of dispersion
	similar to the standard deviation, but is more robust to outliers [2]_.
	The MAD of an empty array is ``numpy.nan``.

	:param x: Input array or object that can be converted to an array.
	:type x: array_like
	:param axis: Axis along which the range is computed. If None, compute
		the MAD over the entire array.
	:param center: A function that will return the central value. The default is to use
		numpy.median. Any user defined function used will need to have the function
		signature ``func(arr, axis)``.
	:param scale: The scaling factor applied to the MAD. The default scale (1.4826)
		ensures consistency with the standard deviation for normally distributed
		data.
	:param nan_policy: Defines how to handle when input contains nan. 'propagate'
		returns nan, 'raise' throws an error, 'omit' performs the
		calculations ignoring nan values.

	:returns: If ``axis=None``, a scalar is returned. If the input contains
		integers or floats of smaller precision than :class:`numpy.float64`, then the
		output data-type is :class:`numpy.float64`. Otherwise, the output data-type is
		the same as that of the input.
	:rtype: scalar or ndarray

	.. note::

		The `center` argument only affects the calculation of the central value
		around which the MAD is calculated. That is, passing in ``center=numpy.mean``
		will calculate the MAD around the mean - it will not calculate the *mean*
		absolute deviation.

	**References**

	.. [1] "Median absolute deviation" https://en.wikipedia.org/wiki/Median_absolute_deviation
	.. [2] "Robust measures of scale" https://en.wikipedia.org/wiki/Robust_measures_of_scale

	**Examples**

	When comparing the behavior of `median_absolute_deviation` with ``numpy.std``,
	the latter is affected when we change a single value of an array to have an
	outlier value while the MAD hardly changes:

	>>> from scipy import stats
	>>> x = stats.norm.rvs(size=100, scale=1, random_state=123456)
	>>> x.std()
	0.9973906394005013
	>>> stats.median_absolute_deviation(x)
	1.2280762773108278
	>>> x[0] = 345.6
	>>> x.std()
	34.42304872314415
	>>> stats.median_absolute_deviation(x)
	1.2340335571164334
	Axis handling example:
	>>> x = numpy.array([[10, 7, 4], [3, 2, 1]])
	>>> x
	array([[10,  7,  4], [ 3,  2,  1],])
	>>> stats.median_absolute_deviation(x)
	array([5.1891, 3.7065, 2.2239])
	>>> stats.median_absolute_deviation(x, axis=None)
	2.9652
	"""

	ad = absolute_deviation(x, axis=axis, center=center, nan_policy=nan_policy)

	if axis is None:
		mad = numpy.median(ad)
	else:
		mad = numpy.median(ad, axis=axis)

	return scale * mad


def absolute_deviation(
		x,
		axis: Optional[int] = 0,
		center: Callable = numpy.median,
		nan_policy: NaNPolicies = "propagate",
		) -> numpy.ndarray:
	"""
	Compute the absolute deviations from the median of the data along the given axis.

	:param x: Input array or object that can be converted to an array.
	:type x: array_like
	:param axis: Axis along which the range is computed. If None, compute
		the MAD over the entire array.
	:param center: A function that will return the central value. The default is to use
		numpy.median. Any user defined function used will need to have the function
		signature ``func(arr, axis)``.
	:param nan_policy: Defines how to handle when input contains nan. 'propagate'
		returns nan, 'raise' throws an error, 'omit' performs the
		calculations ignoring nan values.

	:returns: If ``axis=None``, a scalar is returned. If the input contains
		integers or floats of smaller precision than :class:`numpy.float64`, then the
		output data-type is :class:`numpy.float64`. Otherwise, the output data-type is
		the same as that of the input.
	:rtype: scalar or ndarray

	.. note::

		The `center` argument only affects the calculation of the central value
		around which the MAD is calculated. That is, passing in ``center=numpy.mean``
		will calculate the MAD around the mean - it will not calculate the *mean*
		absolute deviation.
	"""

	x = numpy.asarray(x)

	# Consistent with `numpy.var` and `numpy.std`.
	if not x.size:
		return numpy.nan

	contains_nan, nan_policy = _contains_nan(x, nan_policy)

	if contains_nan and nan_policy == "propagate":
		return numpy.nan

	if contains_nan and nan_policy == "omit":
		# Way faster than carrying the masks around
		arr = numpy.ma.masked_invalid(x).compressed()
	else:
		arr = x

	if axis is None:
		med = center(arr)
		ad = numpy.abs(arr - med)
	else:
		med = numpy.apply_over_axes(center, arr, axis)
		ad = numpy.abs(arr - med)

	return ad


def absolute_deviation_from_median(
		x,
		axis: Optional[int] = 0,
		center: Callable = numpy.median,
		nan_policy: NaNPolicies = "propagate",
		) -> numpy.ndarray:
	"""
	Compute the absolute deviation from the median of each point in the data
	along the given axis, given in terms of the MAD.

	.. seealso::

		https://eurekastatistics.com/using-the-median-absolute-deviation-to-find-outliers/

	:param x: Input array or object that can be converted to an array.
	:type x: array_like
	:param axis: Axis along which the range is computed. If None, compute
		the MAD over the entire array.
	:param center: A function that will return the central value. The default is to use
		numpy.median. Any user defined function used will need to have the function
		signature ``func(arr, axis)``.
	:param nan_policy: Defines how to handle when input contains nan. 'propagate'
		returns nan, 'raise' throws an error, 'omit' performs the
		calculations ignoring nan values.

	:returns: If ``axis=None``, a scalar is returned. If the input contains
		integers or floats of smaller precision than :class:`numpy.float64`, then the
		output data-type is :class:`numpy.float64`. Otherwise, the output data-type is
		the same as that of the input.
	:rtype: scalar or ndarray

	.. note::

		The `center` argument only affects the calculation of the central value
		around which the MAD is calculated. That is, passing in ``center=numpy.mean``
		will calculate the MAD around the mean - it will not calculate the *mean*
		absolute deviation.
	"""  # noqa D400

	ad = absolute_deviation(x, axis=axis, center=center, nan_policy=nan_policy)

	if axis is None:
		mad = numpy.median(ad)
	else:
		mad = numpy.median(ad, axis=axis)

	return ad / mad


def within1min(value1: float, value2: float) -> bool:
	"""
	Returns whether ``value2`` is within one minute of ``value1``.

	:param value1: A time in minutes.
	:param value2: Another time in minutes.
	"""

	if value1 and value2:
		return (float(value1) - 1) < (float(value2)) < (float(value1) + 1)
	else:
		return False
