# stdlib
from typing import Iterable

# 3rd party
import numpy  # type: ignore
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from mathematical.outliers import mad_outliers, quartile_outliers, spss_outliers, stdev_outlier, two_stdev


def to_std_nums(data: Iterable[float]) -> Iterable[float]:
	for value in data:
		if isinstance(value, float):
			yield float(value)
		elif isinstance(value, (int, numpy.signedinteger)):
			yield int(value)
		else:
			raise NotImplementedError(f"Cannot convert {value} of type {type(value)}")


data = pytest.mark.parametrize(
		"data",
		[
				[1, 2, 3, 4, 5],
				[1, 2, 3, 4, 10],
				[1, 2, 3, 4, 50],
				[1, 2, 3, 4, 100],
				[1, 2, 3, 4, 1000],
				[1, 2, 3, 50, 1000],
				]
		)


@data
@pytest.mark.parametrize("threshold", [2, 3])
def test_mad_outliers(data, advanced_data_regression: AdvancedDataRegressionFixture, threshold: int):
	outliers, data_exc_outliers = mad_outliers(data, threshold=threshold)
	advanced_data_regression.check({
			"outliers": list(to_std_nums(outliers)),
			"data_exc_outliers": list(to_std_nums(data_exc_outliers)),
			})


@data
def test_two_stdev(data, advanced_data_regression: AdvancedDataRegressionFixture):
	outliers, data_exc_outliers = two_stdev(data)
	advanced_data_regression.check({
			"outliers": list(to_std_nums(outliers)),
			"data_exc_outliers": list(to_std_nums(data_exc_outliers)),
			})


@data
def test_quartile_outliers(data, advanced_data_regression: AdvancedDataRegressionFixture):
	outliers, data_exc_outliers = quartile_outliers(data)
	advanced_data_regression.check({
			"outliers": list(to_std_nums(outliers)),
			"data_exc_outliers": list(to_std_nums(data_exc_outliers)),
			})


@data
def test_spss_outliers(data, advanced_data_regression: AdvancedDataRegressionFixture):
	extremes, outliers, data_exc_outliers = spss_outliers(data)
	advanced_data_regression.check({
			"extremes": list(to_std_nums(extremes)),
			"outliers": list(to_std_nums(outliers)),
			"data_exc_outliers": list(to_std_nums(data_exc_outliers)),
			})


def test_small_dataset():

	data = [1, None]

	assert mad_outliers(data) == ([], [1])
	assert stdev_outlier(data) == ([], [1])
	assert quartile_outliers(data) == ([], [1])

	with pytest.raises(ValueError, match="Dataset too small"):
		spss_outliers([])

	with pytest.raises(ValueError, match="Dataset too small"):
		spss_outliers([1])
