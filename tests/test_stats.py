# -*- coding: utf-8 -*-
"""
test_init
~~~~~~~~~~~~~~~

Test functions in __init__.py

"""
import numpy
from mathematical import stats

data = [1,2,3,4,5,0,"abc",False, None, numpy.nan]

def test_mean_none():
	assert isinstance(stats.mean_none(data),float)
	assert stats.mean_none(data) == 3.0

def test_median_none():
	assert isinstance(stats.median_none(data),float)
	assert stats.median_none(data) == 3.0

def test_std_none():
	assert isinstance(stats.std_none(data, 0),float)
	assert str(stats.std_none(data, 0))[:5] == "1.4142135623730951"[:5]

def test_percentile_none():
	assert isinstance(stats.percentile_none(data, 25), float)
	assert stats.percentile_none(data, 25) == 2
	assert stats.percentile_none(data, 75) == 4
	assert stats.percentile_none(data, 0) == 1
	assert stats.percentile_none(data, 50) == 3
	assert stats.percentile_none(data, 100) == 5

def test_iqr_none():
	assert isinstance(stats.iqr_none(data),float)
	assert stats.iqr_none(data) == 2.0

def test_mad():
	# Based on example from scipy.median_absolute_deviation docstring
	import scipy.stats
	x = scipy.stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.median_absolute_deviation(x), float)
	assert stats.median_absolute_deviation(x) == 1.2280762773108278
	
def test_ad():
	# Based on example from scipy.median_absolute_deviation docstring
	import scipy.stats
	x = scipy.stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.absolute_deviation(x), numpy.ndarray)
	assert stats.absolute_deviation(x)[0] == 0.6072408011711852

def test_absolute_deviation_from_median():
	# Based on example from scipy.median_absolute_deviation docstring
	import scipy.stats
	x = scipy.stats.norm.rvs(size=100, scale=1, random_state=123456)
	assert isinstance(stats.absolute_deviation_from_median(x), numpy.ndarray)
	assert stats.absolute_deviation_from_median(x)[0] == 0.7330938871222354

def test_within1min():
	assert stats.within1min(10.1, 10.5)
	assert not stats.within1min(10.1, 15.5)

# TODO: pooled_sd, d_cohen, g_hedge, g_durlak_bias, interpret_d


