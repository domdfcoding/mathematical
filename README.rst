=====================
mathematical
=====================

.. start short_desc

**Mathematical tools for Python 📐 🐍 🛠️**

.. end short_desc

Includes tools for calculating mean, median and standard deviation of rows in data frames, detection of outliers, and statistical calculations

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/mathematical/latest?logo=read-the-docs
	:target: https://mathematical.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/mathematical/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/mathematical/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/mathematical/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/mathematical/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/mathematical/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/mathematical/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/mathematical/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/domdfcoding/mathematical/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/mathematical/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/mathematical?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/mathematical?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/mathematical
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mathematical?logo=python&logoColor=white
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/mathematical?logo=anaconda
	:target: https://anaconda.org/domdfcoding/mathematical
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/mathematical?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/mathematical
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/mathematical
	:target: https://github.com/domdfcoding/mathematical/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/mathematical
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/mathematical/v0.5.1
	:target: https://github.com/domdfcoding/mathematical/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/mathematical
	:target: https://github.com/domdfcoding/mathematical/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Downloads

.. end shields

Installation
----------------

.. start installation

``mathematical`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install mathematical

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install mathematical

.. end installation
