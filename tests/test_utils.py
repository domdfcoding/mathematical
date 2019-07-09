# -*- coding: utf-8 -*-
"""
test_utils
~~~~~~~~~~~~~~~

Test functions in utils.py

"""

import numpy, decimal
from mathematical import utils

data = [1,2,3,4,5,0,"abc",False, None, numpy.nan]

def test_magnitude():
	assert isinstance(utils.magnitude(1234), int)
	assert utils.magnitude(1234) == 3

def test_remove_zero():
	assert isinstance(utils.remove_zero(data),list)
	assert utils.remove_zero(data) == [1,2,3,4,5,"abc", numpy.nan]

def test_isint():
	assert isinstance(utils.isint(1),bool)
	assert isinstance(utils.isint(1.0),bool)
	assert utils.isint(1)
	assert utils.isint(1.0)

def test_RepresentsInt():
	assert isinstance(utils.RepresentsInt(1),bool)
	assert isinstance(utils.RepresentsInt(1.0),bool)
	assert isinstance(utils.RepresentsInt("1"),bool)
	assert utils.RepresentsInt(1)
	assert utils.RepresentsInt(1.0)
	assert utils.RepresentsInt("1")
	
def test_rounders():
	assert isinstance(utils.rounders(1234.5678, "0.0"), decimal.Decimal)
	assert str(utils.rounders(1234.5678, "0.0")) == "1234.6"

def test_strip_strings():
	assert isinstance(utils.strip_strings(data), list)
	assert utils.strip_strings(data) == [1,2,3,4,5,0,False, None, numpy.nan]

def test_strip_booleans():
	assert isinstance(utils.strip_booleans(data), list)
	assert utils.strip_booleans(data) == [1,2,3,4,5,0,"abc", None, numpy.nan]

def test_strip_nonetype():
	assert isinstance(utils.strip_nonetype(data), list)
	assert utils.strip_nonetype(data) == [1,2,3,4,5,0,"abc",False, numpy.nan]

def test_strip_none_bool_string():
	assert isinstance(utils.strip_none_bool_string(data), list)
	assert utils.strip_none_bool_string(data) == [1,2,3,4,5,0, numpy.nan]

#TODO: gcd, gcd2, lcm, hcf, hcf2, modInverse

