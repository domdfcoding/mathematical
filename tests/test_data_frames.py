# -*- coding: utf-8 -*-
"""
test_data_frames
~~~~~~~~~~~~~~~

Test functions in data_frames.py

"""
from mathematical.data_frames import *
import copy
import pandas

base_df = pandas.DataFrame(
		[[2444, 8196, 6036, 1757, 5265]],
		columns=["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"])

print(base_df)


def test_df_mean():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Mean"] = base_df.apply(
			df_mean,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Mean"][0] == 4739.6

	# Without Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Mean"] = base_df.apply(df_mean, axis=1)
	assert df["Sample Mean"][0] == 4739.6


def test_df_median():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Median"] = base_df.apply(
			df_median,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Median"][0] == 5265.0

	# Without Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Median"] = base_df.apply(df_median, axis=1)
	assert df["Sample Median"][0] == 5265.0


def test_df_stdev():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Stdev"] = base_df.apply(
			df_stdev,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Stdev"][0] == 2369.3493284022093

	# Without Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Stdev"] = base_df.apply(df_stdev, axis=1)
	assert df["Sample Stdev"][0] == 2369.3493284022093


def test_df_log_stdev():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Log Stdev"] = base_df.apply(
			df_log_stdev,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Log Stdev"][0] == 0.2515430004296598

	# Without Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Log Stdev"] = base_df.apply(df_log_stdev, axis=1)
	assert df["Sample Log Stdev"][0] == 0.2515430004296598


def test_df_percentage():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Percentage"] = base_df.apply(
			df_percentage,
			args=(["Sample 1"], sum([2444, 8196, 6036, 1757, 5265])),
			axis=1)
	assert df["Sample 1 Percentage"][0] == 10.313106591273526


def test_df_log():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample 1 Log"] = base_df.apply(df_log, args=(["Sample 1"],), axis=1)
	assert df["Sample 1 Log"][0] == 3.388101201570516


def test_df_data_points():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Data Points"] = base_df.apply(
			df_data_points,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Data Points"][0] == [2444, 8196, 6036, 1757, 5265]


# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Data Points"] = base_df.apply(df_data_points, axis=1)
# assert df["Sample Data Points"][0] == [2444,8196,6036,1757,5265]

# TODO: df_outliers


def test_df_count():
	# With Columns Specified
	df = copy.deepcopy(base_df)
	df["Sample Count"] = base_df.apply(
			df_count,
			args=(["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],),
			axis=1)
	assert df["Sample Count"][0] == 5

# Without Columns Specified
# df = copy.deepcopy(base_df)
# df["Sample Count"] = base_df.apply(df_count, axis=1)
# assert df["Sample Count"][0] == 5
