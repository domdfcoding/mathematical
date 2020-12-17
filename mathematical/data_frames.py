#!/usr/bin/env python
#
#  date_frames.py
"""
Mathematical operations for :class:`Data Frames <pandas.DataFrame>`.
"""
#
#  Copyright © 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on
# 		http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
# 		Copyright 2016 Jonathan Soma
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
from math import log, log10
from typing import List, Optional, Sequence

# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore

# this package
from mathematical import outliers

pandas.DataFrame.__module__ = "Pandas"
pandas.Series.__module__ = "Pandas"

__all__ = [
		"df_mean",
		"df_median",
		"df_stdev",
		"df_log_stdev",
		"df_percentage",
		"df_log",
		"df_data_points",
		"df_outliers",
		"df_count",
		"df_delta",
		"df_delta_relative",
		"ColumnLabelList",
		"set_display_options",
		]

# Outlier Modes
MAD = 1
QUARTILES = 2
STDEV2 = 3

#: Type hint for the ``column_label_list`` parameter in the ``df_*()`` functions.
ColumnLabelList = Optional[Sequence[str]]


def df_mean(row: pandas.Series, column_label_list: ColumnLabelList = None) -> float:
	"""
	Calculate the mean of each row for the specified columns of a
	:class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Mean"] = data_frame.apply(
				func=df_mean,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate the mean for.

	:return: The mean
	"""  # noqa D400

	if column_label_list is None:
		column_label_list = list(row.index)

	return float(numpy.nanmean(tuple(row[column_label_list])))


def df_median(row: pandas.Series, column_label_list: ColumnLabelList = None) -> float:
	"""
	Calculate the median of each row for the specified columns of a
	:class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Median"] = data_frame.apply(
				func=df_median,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate median for.

	:return: The median
	"""  # noqa D400

	if column_label_list is None:
		column_label_list = list(row.index)

	return float(numpy.nanmedian(tuple(row[column_label_list])))


def df_stdev(row: pandas.Series, column_label_list: ColumnLabelList = None) -> float:
	"""
	Calculate the standard deviation of each row for the specified
	columns of a :class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Stdev"] = data_frame.apply(
				func=df_stdev,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate standard deviation for.

	:return: The standard deviation
	"""  # noqa D400

	if column_label_list is None:
		column_label_list = list(row.index)

	return float(numpy.nanstd(tuple(row[column_label_list])))


def df_log_stdev(row: pandas.Series, column_label_list: ColumnLabelList = None) -> float:
	"""
	Calculate the standard deviation of the log10 values in each row for the
	specified columns of a :class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Log Stdev"] = data_frame.apply(
				func=df_log_stdev,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate standard deviation for.

	:return: The standard deviation
	"""  # noqa D400

	if column_label_list is None:
		column_label_list = list(row.index)

	log_values = [log10(x) if x > 0.0 else numpy.nan for x in row[column_label_list]]
	return float(numpy.nanstd(log_values))


def df_percentage(row: pandas.Series, column_label: str, total: float) -> float:
	"""
	Returns the value of the specified column as a percentage of the given total.

	The total is usually the sum of the specified column.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Bob Percentage"] = data_frame.apply(
				func=df_percentage,
				args=[13, "Bob"],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label: The column to calculate percentage for.
	:param total: The total value.

	:return: Percentage * 100
	"""

	return (row[column_label] / float(total)) * 100.0


def df_log(row: pandas.Series, column_label_list: Sequence[str], base: float = 10) -> float:
	"""
	Calculate the logarithm of the values in each row for the specified
	columns of a :class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Bob Log10"] = data_frame.apply(
				func=df_log,
				args=[["Bob"], 10],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate log for.
	:param base: The logarithmic base.

	:return: The logarithmic value.
	"""  # noqa D400

	if all(row[column_label_list][i] > 0.0 for i in range(len(row[column_label_list]))):
		return log(row[column_label_list], base)
	else:
		return 0


def df_data_points(row: pandas.Series, column_label_list: Sequence[str]) -> List:
	"""
	Compile the values for the specified columns in each row into a list.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Data Points"] = data_frame.apply(
				func=df_data_points,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to calculate standard deviation for.

	:return: The number of data points.
	"""

	return [row[column_label] for column_label in column_label_list]


def df_outliers(
		row: pandas.Series,
		column_label_list: ColumnLabelList = None,
		outlier_mode: int = MAD,
		) -> pandas.Series:
	"""
	Identify outliers in each row.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Outliers"] = data_frame.apply(
				func=df_outliers,
				args=[["Bob", "Alice"]],
				axis=1,
				)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to determine outliers for.
	:param outlier_mode: outlier detection method to use.

	:return: The outliers.
	"""

	if column_label_list is None:
		column_label_list = list(row.index)

	data = row[column_label_list]
	if all(all(y == 0.0 for y in x) for x in data):
		return pandas.Series([[], [0.0] * len(data[0])])

	if outlier_mode == MAD:
		x = outliers.mad_outliers(data)
	elif outlier_mode == QUARTILES:
		x = outliers.quartile_outliers(data)
	elif outlier_mode == STDEV2:
		# outlier classed as more than 2 stdev away from mean
		x = outliers.stdev_outlier(data, rng=2)
	else:
		raise ValueError("Unknown outlier mode.")

	return pandas.Series(list(x))


def df_count(row: pandas.Series, column_label_list: ColumnLabelList = None) -> int:
	"""
	Count the number of occurrences of a non-NaN value in the specified
	columns of a :class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Count"] = data_frame.apply(
			func=df_count,
			args=[["Bob", "Alice"]],
			axis=1,
			)

	:param row: Row of the data frame.
	:param column_label_list: List of column labels to count occurrences in.

	:return: Count of the occurrences of non-NaN values.
	"""  # noqa D400

	if column_label_list is None:
		column_label_list = list(row.index)

	count = 0

	for column_label in column_label_list:
		if row[column_label] and not numpy.isnan(row[column_label]):
			count += 1

	return count


def df_delta(row: pandas.Series, left_column: str, right_column: str) -> float:
	"""
	Calculate the difference between values in the two columns for each row of a
	:class:`data frame <pandas.DataFrame>`.

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Delta"] = data_frame.apply(
				func=df_delta,
				args=["Bob", "Alice"],
				axis=1,
				)

	:param row: Row of the data frame.
	:param left_column:
	:param right_column:

	:return: The difference between ``left_column`` and ``right_column``.

	.. versionadded:: 0.4.0
	"""  # noqa D400

	return row[left_column] - row[right_column]


def df_delta_relative(row: pandas.Series, left_column: str, right_column: str) -> float:
	"""
	Calculate the relative difference between values in the two columns for each row of a
	:class:`data frame <pandas.DataFrame>`::

		(left - right) / right

	Do not call this function directly; use it with
	:meth:`df.apply() <pandas.DataFrame.apply>` instead:

	.. code-block:: python

		data_frame["Rel. Delta"] = data_frame.apply(
				func=df_delta_relative,
				args=["Bob", "Alice"],
				axis=1,
				)

	:param row: Row of the data frame.
	:param left_column:
	:param right_column:

	:return: The relative difference between ``left_column`` and ``right_column``.

	.. versionadded:: 0.4.0
	"""  # noqa D400

	right = row[right_column]

	if right:
		return (row[left_column] - right) / right
	else:
		return float("inf")


def set_display_options(desired_width: int = 300, max_columns: int = 15, max_rows: int = 20):
	"""
	Set the display options for numpy and pandas.

	:param desired_width: The desired maximum output width, in characters.
	:param max_columns: The maximum number of columns to display in a :class:`pandas.DataFrame`.
	:param max_rows: The maximum number of rows to display in a :class:`pandas.DataFrame`.

	.. versionadded:: 0.3.0
	"""

	pandas.set_option("display.width", desired_width)
	numpy.set_printoptions(linewidth=desired_width)
	pandas.options.display.max_columns = max_columns
	pandas.options.display.max_rows = max_rows
