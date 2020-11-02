# Python test set -- built-in functions

# stdlib
import itertools
import pickle
import sys

# 3rd party
import pytest
from domdf_python_tools.testing import min_version

# this package
from mathematical.utils import FRange


def assert_iterators_equal(xs, ys, test_id, limit=None):
	# check that an iterator xs matches the expected results ys,
	# up to a given limit.
	if limit is not None:
		xs = itertools.islice(xs, limit)
		ys = itertools.islice(ys, limit)
	sentinel = object()
	pairs = itertools.zip_longest(xs, ys, fillvalue=sentinel)
	for i, (x, y) in enumerate(pairs):
		if x == y:
			continue
		elif x == sentinel:
			pytest.fail(f"{test_id}: iterator ended unexpectedly at position {i}; expected {y}")
		elif y == sentinel:
			pytest.fail(f"{test_id}: unexpected excess element {x} at position {i}")
		else:
			pytest.fail(f"{test_id}: wrong element at position {i}; expected {y}, got {x}")


def test_range():
	assert list(FRange(3)) == [0, 1, 2]
	assert list(FRange(1, 5)) == [1, 2, 3, 4]
	assert list(FRange(0)) == []
	assert list(FRange(-3)) == []
	assert list(FRange(1, 10, 3)) == [1, 4, 7]
	assert list(FRange(5, -5, -3)) == [5, 2, -1, -4]

	a = 10
	b = 100
	c = 50

	assert list(FRange(a, a + 2)) == [a, a + 1]
	assert list(FRange(a + 2, a, -1)) == [a + 2, a + 1]
	assert list(FRange(a + 4, a, -2)) == [a + 4, a + 2]

	seq = list(FRange(a, b, c))
	assert a in seq
	assert b not in seq
	assert len(seq) == 2

	seq = list(FRange(b, a, -c))
	assert b in seq
	assert a not in seq
	assert len(seq) == 2

	seq = list(FRange(-a, -b, -c))
	assert -a in seq
	assert -b not in seq
	assert len(seq) == 2

	with pytest.raises(TypeError):
		FRange()  # type: ignore
	with pytest.raises(TypeError):
		FRange(1, 2, 3, 4)  # type: ignore
	with pytest.raises(ValueError):
		FRange(1, 2, 0)

	FRange(0.0, 2, 1)
	FRange(1, 2.0, 1)
	FRange(1, 2, 1.0)

	with pytest.raises(ValueError, match="Value 1e\\+100 too large for 'start'"):
		FRange(1e100, 1e101, 1e101)

	with pytest.raises(ValueError, match="could not convert string to float: 'spam'"):
		FRange(0, "spam")  # type: ignore
	with pytest.raises(ValueError, match="could not convert string to float: 'spam'"):
		FRange(0, 42, "spam")  # type: ignore

	with pytest.raises(ValueError, match="Value .* too large for 'stop'"):
		FRange(0, sys.maxsize, sys.maxsize - 1)

	with pytest.raises(ValueError, match="Value .* too large for 'start'"):
		FRange(-sys.maxsize, sys.maxsize, 2)


def test_range_constructor_error_messages():
	with pytest.raises(TypeError, match="Invalid argument types."):
		FRange()  # type: ignore

	with pytest.raises(TypeError, match="__init__\\(\\) takes from 1 to 4 positional arguments but 7 were given"):
		FRange(1, 2, 3, 4, 5, 6)  # type: ignore


a = int(10 * sys.maxsize)
b = int(100 * sys.maxsize)
c = int(50 * sys.maxsize)


@pytest.mark.parametrize(
		"values",
		[
				(10**20, 10**20 + 10, 3),
				(10**20 + 10, 10**20, 3),
				(10**20, 10**20 + 10, -3),
				(10**20 + 10, 10**20, -3),
				(a, a + 2),
				(a + 2, a, -1),
				(a + 4, a, -2),
				(a, b, c),
				(b, a, -c),
				(-a, -b, -c),
				]
		)
def test_large_operands_start(values):
	with pytest.raises(ValueError, match="Value .* too large for 'start'"):
		FRange(*values)


@pytest.mark.parametrize("values", [
		(-2**100, ),
		(0, -2**100),
		(0, 2**100, -1),
		])
def test_large_operands_stop(values):
	with pytest.raises(ValueError, match="Value .* too large for 'stop'"):
		FRange(*values)


def test_large_range():
	a = -sys.maxsize
	b = sys.maxsize

	with pytest.raises(ValueError, match="Value .* too large for 'start'"):
		FRange(a, b)

	a = 0
	b = 2 * sys.maxsize

	with pytest.raises(ValueError, match="Value .* too large for 'stop'"):
		FRange(a, b)

	a = 0
	b = sys.maxsize**10
	c = 2 * sys.maxsize

	with pytest.raises(ValueError, match="Value .* too large for 'stop'"):
		FRange(a, b, c)

	a = sys.maxsize**10
	b = 0
	c = -2 * sys.maxsize

	with pytest.raises(ValueError, match="Value .* too large for 'start'"):
		FRange(a, b, c)


def test_invalid_invocation():
	with pytest.raises(TypeError):
		FRange()  # type: ignore
	with pytest.raises(TypeError):
		FRange(1, 2, 3, 4)  # type: ignore
	with pytest.raises(ValueError):
		FRange(1, 2, 0)
	a = int(10 * sys.maxsize)
	with pytest.raises(ValueError):
		FRange(a, a + 1, int(0))


def test_index():
	u = FRange(2)
	assert u.index(0) == 0
	assert u.index(1) == 1
	with pytest.raises(ValueError):
		u.index(2)

	u = FRange(-2, 3)
	assert u.count(0) == 1
	assert u.index(0) == 2
	with pytest.raises(TypeError):
		u.index()  # type: ignore

	class BadExc(Exception):
		pass

	class BadCmp:

		def __eq__(self, other):
			if other == 2:
				raise BadExc()
			return False

	a = FRange(4)
	with pytest.raises(ValueError, match=".*BadCmp object at 0x.*> is not in range"):
		a.index(BadCmp())  # type: ignore

	a = FRange(-2, 3)
	assert a.index(0) == 2
	assert FRange(1, 10, 3).index(4) == 1
	assert FRange(1, -10, -3).index(-5) == 2


@min_version("3.8", "Behaviour changed in Python 3.8")
def test_user_index_method():
	smallnum = 42

	# User-defined class with an __index__ method
	class I:

		def __init__(self, n):
			self.n = int(n)

		def __index__(self):
			return self.n

	assert list(FRange(I(smallnum), I(smallnum + 1))) == [smallnum]  # type: ignore

	# User-defined class with a failing __index__ method
	class IX:

		def __index__(self):
			raise RuntimeError

	with pytest.raises(RuntimeError):
		FRange(IX())  # type: ignore

	# User-defined class with an invalid __index__ method
	class IN:

		def __index__(self):
			return "not a number"

	with pytest.raises(TypeError):
		FRange(IN())  # type: ignore


def test_count():
	assert FRange(3).count(-1) == 0
	assert FRange(3).count(0) == 1
	assert FRange(3).count(1) == 1
	assert FRange(3).count(2) == 1
	assert FRange(3).count(3) == 0
	assert type(FRange(3).count(-1)) is int
	assert type(FRange(3).count(1)) is int
	assert FRange(3).index(1) == 1


@pytest.mark.parametrize(
		"value, expects",
		[
				(FRange(1), "FRange(0.0, 1.0)"),
				(FRange(1, 2), "FRange(1.0, 2.0)"),
				(FRange(1, 2, 3), "FRange(1.0, 2.0, 3.0)"),
				]
		)
def test_repr(value, expects):
	assert repr(value) == expects


def test_pickling():
	testcases = [(13, ), (0, 11), (-22, 10), (20, 3, -1), (13, 21, 3), (-2, 2, 2)]
	for proto in range(pickle.HIGHEST_PROTOCOL + 1):
		for t in testcases:
			r = FRange(*t)
			assert list(pickle.loads(pickle.dumps(r, proto))) == list(r)


def test_odd_bug():
	# This used to raise a "SystemError: NULL result without error"
	# because the range validation step was eating the exception
	# before NULL was returned.
	with pytest.raises(TypeError):
		FRange([], 1, -1)  # type: ignore


def test_strided_limits():
	r = FRange(0, 101, 2)
	assert 0 in r
	assert 1 not in r
	assert 2 in r
	assert 99 not in r
	assert 100 in r
	assert 101 not in r

	r = FRange(0, -20, -1)
	assert 0 in r
	assert -1 in r
	assert -19 in r
	assert -20 not in r

	r = FRange(0, -20, -2)
	assert -18 in r
	assert -19 not in r
	assert -20 not in r


def test_empty():
	r = FRange(0)
	assert 0 not in r
	assert 1 not in r

	r = FRange(0, -10)
	assert 0 not in r
	assert -1 not in r
	assert 1 not in r


#
# def test_slice():
# 	def check(start, stop, step=None):
# 		i = slice(start, stop, step)
# 		assert list(r[i]) == list(r)[i]
# 		assert len(r[i]) == len(list(r)[i])
#
# 	for r in [FRange(10),
# 			  FRange(0),
# 			  FRange(1, 9, 3),
# 			  FRange(8, 0, -3),
# 			  ]:
# 		check(0, 2)
# 		check(0, 20)
# 		check(1, 2)
# 		check(20, 30)
# 		check(-30, -20)
# 		check(-1, 100, 2)
# 		check(0, -1)
# 		check(-1, -3, -1)


def test_contains():
	r = FRange(10)
	assert 0 in r
	assert 1 in r
	assert 5.0 in r
	assert 5.1 not in r
	assert -1 not in r
	assert 10 not in r
	assert '' not in r

	r = FRange(9, -1, -1)
	assert 0 in r
	assert 1 in r
	assert 5.0 in r
	assert 5.1 not in r
	assert -1 not in r
	assert 10 not in r
	assert '' not in r

	r = FRange(0, 10, 2)
	assert 0 in r
	assert 1 not in r
	assert 5.0 not in r
	assert 5.1 not in r
	assert -1 not in r
	assert 10 not in r
	assert '' not in r

	r = FRange(9, -1, -2)
	assert 0 not in r
	assert 1 in r
	assert 5.0 in r
	assert 5.1 not in r
	assert -1 not in r
	assert 10 not in r
	assert '' not in r


@pytest.mark.parametrize(
		"left, right",
		[
				(FRange(0, 100, 2), FRange(98, -2, -2)),
				(FRange(0, 100), FRange(99, -1, -1)),
				(FRange(10, 100, 2), FRange(98, 8, -2)),
				(FRange(10), FRange(9, -1, -1)),
				(FRange(0), FRange(0, 0, -1)),
				(FRange(100, 100, -5), FRange(100, 100, 5)),
				(FRange(1, 9, 3), FRange(7, -2, -3)),
				(FRange(8, 0, -3), FRange(2, 11, 3)),
				]
		)
def test_reverse_iteration(left, right):
	# assert reversed(left) == right
	assert list(reversed(left)) == list(left)[::-1]


#
# def test_issue11845():
# 	r = FRange(*slice(1, 18, 2).indices(20))
# 	values = {None, 0, 1, -1, 2, -2, 5, -5, 19, -19,
# 			  20, -20, 21, -21, 30, -30, 99, -99}
# 	for i in values:
# 		for j in values:
# 			for k in values - {0}:
# 				r[i:j:k]


def test_comparison():
	test_ranges = [
			FRange(0),
			FRange(0, -1),
			FRange(1, 1, 3),
			FRange(1),
			FRange(5, 6),
			FRange(5, 6, 2),
			FRange(5, 7, 2),
			FRange(2),
			FRange(0, 4, 2),
			FRange(0, 5, 2),
			FRange(0, 6, 2)
			]
	test_tuples = list(map(list, test_ranges))  # type: ignore

	# Check that equality of ranges matches equality of the corresponding
	# tuples for each pair from the test lists above.

	for a_r, a_t in zip(test_ranges, test_tuples):
		for b_r, b_t in zip(test_ranges, test_tuples):
			if a_r == b_r:
				print(f"{a_r} == {b_r}")
				print(f"{a_t} == {b_t}?")
				assert a_t == b_t
			else:
				print(f"{a_r} != {b_r}")
				print(f"{a_t} != {b_t}?")
				assert a_t != b_t

	ranges_eq = [a == b for a in test_ranges for b in test_ranges]
	tuples_eq = [a == b for a in test_tuples for b in test_tuples]
	assert ranges_eq == tuples_eq

	# Check that != correctly gives the logical negation of ==
	ranges_ne = [a != b for a in test_ranges for b in test_ranges]
	assert ranges_ne == [not x for x in ranges_eq]

	# Equal ranges should have equal hashes.
	for a in test_ranges:
		for b in test_ranges:
			if a == b:
				assert hash(a) == hash(b)

	# Ranges are unequal to other types (even sequence types)
	assert not FRange(0) == ()
	assert not () == FRange(0)
	assert not FRange(2) == [0, 1]

	# Order comparisons are not implemented for ranges.
	with pytest.raises(TypeError):
		FRange(0) < FRange(0)  # type: ignore
	with pytest.raises(TypeError):
		FRange(0) > FRange(0)  # type: ignore
	with pytest.raises(TypeError):
		FRange(0) <= FRange(0)  # type: ignore
	with pytest.raises(TypeError):
		FRange(0) >= FRange(0)  # type: ignore


@pytest.mark.parametrize(
		"rangeobj, start, stop, step",
		[
				(FRange(0), 0, 0, 1),
				(FRange(10), 0, 10, 1),
				(FRange(-10), 0, -10, 1),
				(FRange(0, 10, 1), 0, 10, 1),
				(FRange(0, 10, 3), 0, 10, 3),
				(FRange(10, 0, -1), 10, 0, -1),
				(FRange(10, 0, -3), 10, 0, -3),
				(FRange(True), 0, 1, 1),
				(FRange(False, True), 0, 1, 1),
				(FRange(False, True, True), 0, 1, 1),
				]
		)
def test_attributes(rangeobj, start, stop, step):
	# test the start, stop and step attributes of range objects

	assert rangeobj.start == start
	assert rangeobj.stop == stop
	assert rangeobj.step == step
	assert type(rangeobj.start) is float
	assert type(rangeobj.stop) is float
	assert type(rangeobj.step) is float

	with pytest.raises(AttributeError):
		rangeobj.start = 0
	with pytest.raises(AttributeError):
		rangeobj.stop = 10
	with pytest.raises(AttributeError):
		rangeobj.step = 1

	with pytest.raises(AttributeError):
		del rangeobj.start
	with pytest.raises(AttributeError):
		del rangeobj.stop
	with pytest.raises(AttributeError):
		del rangeobj.step
