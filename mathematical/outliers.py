#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  outliers.py
"""Outlier Detection Functions"""
#
#  Copyright 2018-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  mad_outliers based on https://eurekastatistics.com/using-the-median-absolute-deviation-to-find-outliers/
#		Copyright 2013 Peter Rosenmai
#
#  quartile_outliers based on http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
#		Copyright 2012 NIST
#
#  spss_outliers based on http://www.unige.ch/ses/sococ/cl/spss/concepts/outliers.html
#		Copyright 2018 Eugene Horber, U. of Geneva
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
#

import numpy
from . import utils
from . import stats

def mad_outliers(dataset, strip_zero=True, threshold=3,):
	"""
	Using the Median Absolute Deviation to Find Outliers
	
	:param dataset:
	:type dataset: list
	:param threshold: The multiple of MAD above which values are considered to be outliers
		Leys et al (2013) make the following recommendations:
			1 In univariate statistics, the Median Absolute Deviation is the most robust
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
		See https://dipot.ulb.ac.be/dspace/bitstream/2013/139499/1/Leys_MAD_final-libre.pdf
	:type threshold: int
	
	:return:
	"""
	
	dataset = utils.strip_none_bool_string(dataset)
	
	if strip_zero:
		dataset = utils.remove_zero(dataset)
	
	if len(dataset) < 2:
		return [], dataset
		
	abs_mad = stats.absolute_deviation_from_median(dataset, scale=1)
	
	outliers = []
	data_exc_outliers = []
	
	for mad_value, value in zip(abs_mad, dataset):
		if mad_value > threshold or -threshold > mad_value:
			outliers.append(value)
		else:
			data_exc_outliers.append(value)
	
	return outliers, data_exc_outliers


def two_stdev(dataset, strip_zero=True):
	"""
	Outliers are greater than 2x stdev from mean
	
	:param dataset:
	
	:return:
	"""
	
	return stdev_outlier(dataset, strip_zero=strip_zero)
	

def stdev_outlier(dataset, strip_zero=True, rng=int(2)):
	"""
	Outliers are greater than rng*stdev from mean
	
	:param dataset:
	:param rng:
	
	:return:
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


def quartile_outliers(dataset, strip_zero=True):
	"""
	outliers are more than 3x inter-quartile range from upper or lower quartile
	
	:param dataset:
	
	:return:
	"""
	
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


def spss_outliers(dataset, strip_zero=True, mode="all"):
	"""
	Based on IBM SPSS method for detecting outliers
	Outliers more than 1.5*IQR from Q1 or Q3
	"Extreme values" more than 3*IQR from Q1 or Q3
	
	:param dataset:
	:param mode:
	
	:return:
	"""
	
	if len(dataset) < 2:
		raise ValueError("Dataset too small")
	
	if list(set(dataset)) in [None, 0.0, '', 0]:
		return float("nan")
	
	for i in range(2):
		dataset = [x for x in dataset if x is not None]
		for val in dataset:
			if val in ['', 0.0, 0]:
				dataset.remove(val)
	if len(dataset) == 0:
		return float('nan')
	elif dataset == [None]:
		return float('nan')
	
	q1 = numpy.percentile(dataset, 25)
	#	print(q1)
	q3 = numpy.percentile(dataset, 75)
	#	print(q3)
	iq = q3 - q1
	#	print(iq)
	
	upper_outlier_fence = q3 + (1.5 * iq)
	lower_outlier_fence = q3 - (1.5 * iq)
	
	upper_extreme_fence = q3 + (3 * iq)
	lower_extreme_fence = q3 - (3 * iq)
	
	outliers = []
	extremes = []
	data_exc_outliers = []
	
	for value in dataset:
		if not lower_extreme_fence < value < (upper_extreme_fence):
			extremes.append(value)
		elif not lower_outlier_fence < value < (upper_outlier_fence):
			outliers.append(value)
		else:
			data_exc_outliers.append(value)
	
	return extremes, outliers, data_exc_outliers


def main(args):
	# my_data = [70,72,74,76,80,114]
	my_data = [1, 2, 3, 3, 4, 4, 4, 5, 5.5, 6, 6, 6.5, 7, 7, 7.5, 8, 9, 12, 52, 90]
	#	print("two stdev")
	#	print(two_stdev(my_data))
	#	print(numpy.mean(two_stdev(my_data)[1]))
	#	print(numpy.median(two_stdev(my_data)[1]))
	#	print("mad")
	#	print(mad_outliers(my_data))
	#	print(numpy.mean(mad_outliers(my_data)[1]))
	#	print(numpy.median(mad_outliers(my_data)[1]))
	#	print("quartile")
	#	print(quartile_outliers(my_data))
	#	print(numpy.mean(quartile_outliers(my_data)[1]))
	#	print(numpy.median(quartile_outliers(my_data)[1]))
	
	print(spss_outliers(my_data))
	
	return 0

if __name__ == '__main__':
	import sys
	
	sys.exit(main(sys.argv))
