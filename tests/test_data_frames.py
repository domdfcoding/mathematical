# -*- coding: utf-8 -*-
"""
test_data_frames
~~~~~~~~~~~~~~~

Test functions in data_frames.py

"""

import copy

import pandas
import pytest

from mathematical.data_frames import (
	df_count, df_data_points, df_log, df_log_stdev, df_mean, df_median, df_percentage,
	df_stdev,
	)


@pytest.fixture(scope="function")
def base_df():
	return pandas.DataFrame(
			[[2444, 8196, 6036, 1757, 5265]],
			columns=["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"])

# print(base_df())


parametrize = [
		("Sample Mean", 4739.6, df_mean),
		("Sample Median", 5265.0, df_median),
		("Sample Stdev", 2369.3493284022093, df_stdev),
		("Sample Log Stdev", 0.2515430004296598, df_log_stdev),
		]


@pytest.mark.parametrize("col_name, expected, function", [
		*parametrize,
		("Sample Data Points", [2444, 8196, 6036, 1757, 5265], df_data_points),
		("Sample Count", 5, df_count),
		])
def test_with_columns(col_name, expected, function, base_df):
	# With Columns Specified
	print(function)
	base_df[col_name] = base_df.apply(
			function,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert base_df[col_name][0] == expected


@pytest.mark.parametrize("col_name, expected, function", parametrize)
def test_without_columns(col_name, expected, function, base_df):
	# Without Columns Specified
	base_df[col_name] = base_df.apply(function, axis=1)
	assert base_df[col_name][0] == expected


def test_df_percentage(base_df):
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Percentage"] = base_df.apply(
			df_percentage,
			args=(["Sample 1"], sum([2444, 8196, 6036, 1757, 5265])),
			axis=1)
	assert df["Sample 1 Percentage"][0] == 10.313106591273526


def test_df_log(base_df):
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Log"] = base_df.apply(df_log, args=(["Sample 1"],), axis=1)
	assert df["Sample 1 Log"][0] == 3.388101201570516


# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Data Points"] = base_df.apply(df_data_points, axis=1)
# assert df["Sample Data Points"][0] == [2444,8196,6036,1757,5265]

# TODO: df_outliers

# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Count"] = base_df.apply(df_count, axis=1)
# assert df["Sample Count"][0] == 5
