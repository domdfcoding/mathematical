"""
test_stats
~~~~~~~~~~~~~~~

Test functions in stats.py

"""
# 3rd party
import numpy  # type: ignore
import pytest

# this package
from mathematical import stats

data = [1, 2, 3, 4, 5, 0, "abc", False, None, numpy.nan]


def test_mean_none():
	assert isinstance(stats.mean_none(data), float)
	assert stats.mean_none(data) == 3.0


def test_median_none():
	assert isinstance(stats.median_none(data), float)
	assert stats.median_none(data) == 3.0


def test_std_none():
	assert isinstance(stats.std_none(data, 0), float)
	assert str(stats.std_none(data, 0))[:5] == "1.4142135623730951"[:5]


@pytest.mark.parametrize("percentile, expects", [
		(25, 2),
		(75, 4),
		(0, 1),
		(50, 3),
		(100, 5),
		])
def test_percentile_none(percentile, expects):
	assert isinstance(stats.percentile_none(data, percentile), float)
	assert stats.percentile_none(data, percentile) == expects


@pytest.mark.parametrize("data", [0, 5, 10, 20, 50.0, 100])
def test_percentile_none_too_small(data):
	with pytest.raises(ValueError, match="Dataset too small"):
		stats.percentile_none([data], 10)


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], 20.480342879074183),
				([25, 75, 50], [30, 80, 48, 52], 19.201779431431177),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					7.410343746712728),
				]
		)
def test_pooled_sd(sample1, sample2, expected):
	assert stats.pooled_sd(sample1, sample2) == expected
	assert stats.pooled_sd(sample1, sample2, weighted=False) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], 20.480342879074183),
				([25, 75, 50], [30, 80, 48, 52], 18.950373786990763),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					7.410343746712728),
				]
		)
def test_pooled_sd_weighted(sample1, sample2, expected):
	assert stats.pooled_sd(sample1, sample2, weighted=True) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.1632993161855453),
				([25, 75, 50], [30, 80, 48, 52], -0.12247448713915889),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-1.001751432800361),
				]
		)
def test_d_cohen(sample1, sample2, expected):
	assert stats.d_cohen(sample1, sample2, which=1) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.1632993161855453),
				([25, 75, 50], [30, 80, 48, 52], -0.12247448713915889),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-1.001751432800361),
				]
		)
def test_d_cohen_which_2(sample1, sample2, expected):
	assert stats.d_cohen(sample1, sample2, which=1) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.1632993161855453),
				([25, 75, 50], [30, 80, 48, 52], -0.12247448713915889),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-1.001751432800361),
				]
		)
def test_d_cohen_second_stdev(sample1, sample2, expected):
	assert stats.d_cohen(sample1, sample2, which=1) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], 0.1632993161855453),
				([25, 75, 50], [30, 80, 48, 52], 0.12247448713915889),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					1.001751432800361),
				]
		)
def test_d_cohen_2_tailed(sample1, sample2, expected):
	assert stats.d_cohen(sample1, sample2, tail=2) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.16275769175423196),
				([25, 75, 50], [30, 80, 48, 52], -0.13019626690991867),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-0.6859780743084032),
				]
		)
def test_d_cohen_pooled(sample1, sample2, expected):
	assert stats.d_cohen(sample1, sample2, pooled=True) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.16275769175423196),
				([25, 75, 50], [30, 80, 48, 52], -0.1319235191928628),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-0.6859780743084032),
				]
		)
def test_g_hedge(sample1, sample2, expected):
	assert stats.g_hedge(sample1, sample2) == expected


@pytest.mark.parametrize(
		"sample1, sample2, expected",
		[
				([25, 75, 50], [30, 80, 50], -0.10631287906961533),
				([25, 75, 50], [30, 80, 48, 52], -0.09389113561651125),
				([301, 298, 295, 297, 304, 305, 309, 298, 291, 299, 293, 304
					], [302, 309, 324, 313, 312, 310, 305, 298, 299, 300, 289, 294],
					-0.6341266242324826),
				]
		)
def test_g_durlak_bias(sample1, sample2, expected):
	g = stats.g_hedge(sample1, sample2)
	assert stats.g_durlak_bias(g, len(sample1) + len(sample2)) == expected


def test_iqr_none():
	assert isinstance(stats.iqr_none(data), float)
	assert stats.iqr_none(data) == 2.0


def test_mad():
	scipy_stats = pytest.importorskip("scipy.stats")

	# Based on example from scipy.median_absolute_deviation docstring
	x = scipy_stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.median_absolute_deviation(x), float)
	assert stats.median_absolute_deviation(x) == 1.2280762773108278


def test_ad():
	scipy_stats = pytest.importorskip("scipy.stats")

	# Based on example from scipy.median_absolute_deviation docstring
	x = scipy_stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.absolute_deviation(x), numpy.ndarray)
	assert stats.absolute_deviation(x)[0] == 0.6072408011711852


def test_absolute_deviation_from_median():
	scipy_stats = pytest.importorskip("scipy.stats")

	# Based on example from scipy.median_absolute_deviation docstring
	x = scipy_stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.absolute_deviation_from_median(x), numpy.ndarray)
	assert stats.absolute_deviation_from_median(x)[0] == 0.7330938871222354


def test_within1min():
	assert stats.within1min(10.1, 10.5)
	assert not stats.within1min(10.1, 15.5)


# TODO: pooled_sd, d_cohen, g_hedge, g_durlak_bias, interpret_d
