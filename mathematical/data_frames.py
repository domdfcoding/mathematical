#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  date_frames.py
"""Mathematical Operations for Data Frames"""
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on
#		http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
#		Copyright 2016 Jonathan Soma
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

# Outlier Modes
MAD = 1
QUARTILES = 2
STDEV2 = 3

def df_mean(row, column_label_list=None):
	"""
	Calculate the mean of each row for the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Mean"] = data_frame.apply(df_mean, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate mean for
	:type column_label_list: list

	:return: Mean
	:rtype: float
	"""
	
	from numpy import nanmean
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	return nanmean(row[column_label_list])


def df_median(row, column_label_list=None):
	"""
	Calculate the median of each row for the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Median"] = data_frame.apply(df_median, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate median for
	:type column_label_list: list

	:return: Median
	:rtype: float
	"""
	
	from numpy import nanmedian
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	return nanmedian(row[column_label_list])


def df_stdev(row, column_label_list=None):
	"""
	Calculate the standard deviation of each row for the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Stdev"] = data_frame.apply(df_stdev, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate standard deviation for
	:type column_label_list: list

	:return: Standard deviation
	:rtype: float
	"""
	
	from numpy import nanstd
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	return nanstd(row[column_label_list])


def df_log_stdev(row, column_label_list=None):
	"""
	Calculate the standard deviation of the log10 values in each row for the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Log Stdev"] = data_frame.apply(df_log_stdev, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate standard deviation for
	:type column_label_list: list

	:return: Standard deviation
	:rtype: float
	"""
	
	from numpy import nanstd, nan
	from math import log10
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	return nanstd([log10(x) if x > 0.0 else nan for x in row[column_label_list]])


def df_percentage(row, column_label, total):
	"""
	Returns the value of the specified column as a percentage of the given total
	The total is usually the sum of the specified column

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Bob Percentage"] = data_frame.apply(df_percentage, args=(
				13, "Bob"), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label: column label to calculate percentage for
	:type column_label: str
	:param total: total value
	:type column_label: str

	:return: Percentage * 100
	:rtype: float
	"""
	
	return (row[column_label] / float(total)) * 100.0


def df_log(row, column_label_list, base=10):
	"""
	Calculate the logarithm of the values in each row for the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Bob Log10"] = data_frame.apply(df_log, args=(
				["Bob"],10), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate log for
	:type column_label_list: list
	:param base: logarithmic base
	:type base: float

	:return: logarithmic value
	:rtype: float
	"""

	from math import log
	
	if all(row[column_label_list][i] > 0.0 for i in range(len(row[column_label_list]))):
		return log(row[column_label_list], base)
	else:
		return 0


def df_data_points(row, column_label_list):
	"""
	Compile the values for the specified columns in each row into a list

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Data Points"] = data_frame.apply(df_data_points, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to calculate standard deviation for
	:type column_label_list: list

	:return: data points
	:rtype: list
	"""
	
	return [row[column_label] for column_label in column_label_list]


def df_outliers(row, column_label_list=None, outlier_mode=MAD):
	"""
	Identify outliers in each row

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Outliers"] = data_frame.apply(df_outliers, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to determine outliers for
	:type column_label_list: list
	:param outlier_mode: outlier detection method to use
	:type outlier_mode: int

	:return: outliers
	:rtype: pandas.core.series.Series
	"""
	
	import pandas as pd
	from . import outliers
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	data = row[column_label_list]
	if all(all(y == 0.0 for y in x) for x in data):
		return pd.Series([[], [0.0]*len(data[0])])
	
	if outlier_mode == MAD:
		x = outliers.mad_outliers(data)
	elif outlier_mode == QUARTILES:
		x = outliers.quartile_outliers(data)
	elif outlier_mode == STDEV2:
		x = outliers.stdev_outlier(data, 2)  # outlier classed as more than 2 stdev away from mean
	else:
		return None
	
	return pd.Series(list(x))


def df_count(row, column_label_list=None):
	"""
	Count the number of occurrences of a non-NaN value in the specified columns of a data frame

	Do not call this function directly; use it with df.apply() instead.

	data_frame["Count"] = data_frame.apply(df_count, args=(
				["Bob", "Alice"],), axis=1)

	:param row: row of the data frame
	:type row: pandas.core.series.Series
	:param column_label_list: list of column labels to count occurrences in
	:type column_label_list: list

	:return: Count of the occurrences of non-NaN values
	:rtype: int
	"""
	
	import numpy
	
	if column_label_list is None:
		column_label_list = list(row.index)
	
	count = 0
	for column_label in column_label_list:
		if row[column_label] and not numpy.isnan(row[column_label]):
			count += 1
	return count

