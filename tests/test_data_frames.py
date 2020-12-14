"""
test_data_frames
~~~~~~~~~~~~~~~~~~

Test functions in data_frames.py

"""

# stdlib
import copy
import math

# 3rd party
import pandas  # type: ignore
import pytest

# this package
from mathematical.data_frames import (
		df_count,
		df_data_points,
		df_delta,
		df_delta_relative,
		df_log,
		df_log_stdev,
		df_mean,
		df_median,
		df_percentage,
		df_stdev
		)


@pytest.fixture()
def base_df():
	return pandas.DataFrame(
			[[2444, 8196, 6036, 1757, 5265]],
			columns=["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],
			)


# print(base_df())

parametrize = [
		("Sample Mean", 4739.6, df_mean),
		("Sample Median", 5265.0, df_median),
		("Sample Stdev", 2369.3493284022093, df_stdev),
		("Sample Log Stdev", 0.2515430004296598, df_log_stdev),
		]


@pytest.mark.parametrize(
		"col_name, expected, function",
		[
				*parametrize,
				("Sample Data Points", [2444, 8196, 6036, 1757, 5265], df_data_points),
				("Sample Count", 5, df_count),
				]
		)
def test_with_columns(col_name, expected, function, base_df):
	# With Columns Specified
	print(function)
	base_df[col_name] = base_df.apply(
			function, args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"], ), axis=1
			)
	assert base_df[col_name][0] == expected


@pytest.mark.parametrize("col_name, expected, function", parametrize)
def test_without_columns(col_name, expected, function, base_df):
	# Without Columns Specified
	base_df[col_name] = base_df.apply(function, axis=1)
	assert base_df[col_name][0] == expected


def test_df_percentage(base_df):
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Percentage"] = df.apply(
			df_percentage,
			args=(["Sample 1"], sum([2444, 8196, 6036, 1757, 5265])),
			axis=1,
			)
	assert df["Sample 1 Percentage"][0] == 10.313106591273526


def test_df_log(base_df):
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Log"] = df.apply(df_log, args=(["Sample 1"], ), axis=1)
	assert df["Sample 1 Log"][0] == 3.388101201570516


def test_df_delta(base_df):
	df = copy.deepcopy(base_df)
	df["Sample 1/2 delta"] = df.apply(df_delta, args=("Sample 1", "Sample 2"), axis=1)
	assert df["Sample 1/2 delta"][0] == -5752

	df = copy.deepcopy(base_df)
	df["Sample 1/2 delta"] = df.apply(df_delta, args=("Sample 2", "Sample 1"), axis=1)
	assert df["Sample 1/2 delta"][0] == 5752


def test_df_delta_relative(base_df):
	df = copy.deepcopy(base_df)
	df["Sample 1/2 rel. delta"] = df.apply(df_delta_relative, args=("Sample 1", "Sample 2"), axis=1)
	assert df["Sample 1/2 rel. delta"][0] == -0.7018057589067838

	df = copy.deepcopy(base_df)
	df["Sample 1/2 rel. delta"] = df.apply(df_delta_relative, args=("Sample 2", "Sample 1"), axis=1)
	assert df["Sample 1/2 rel. delta"][0] == 2.353518821603928

	df = copy.deepcopy(base_df)
	df["Sample 1"][0] = 0
	df["Sample 1/2 rel. delta"] = df.apply(df_delta_relative, args=("Sample 2", "Sample 1"), axis=1)
	assert math.isinf(df["Sample 1/2 rel. delta"][0])


# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Data Points"] = df.apply(df_data_points, axis=1)
# assert df["Sample Data Points"][0] == [2444,8196,6036,1757,5265]

# TODO: df_outliers

# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Count"] = df.apply(df_count, axis=1)
# assert df["Sample Count"][0] == 5
