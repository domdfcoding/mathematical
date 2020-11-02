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
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/mathematical/latest?logo=read-the-docs
	:target: https://mathematical.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/mathematical/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/mathematical/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/mathematical
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/mathematical/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/mathematical/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/mathematical/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/mathematical/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/mathematical/requirements/?branch=master
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/mathematical/v0.2.0
	:target: https://github.com/domdfcoding/mathematical/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/mathematical
	:target: https://github.com/domdfcoding/mathematical/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

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

		$ conda config --add channels http://conda.anaconda.org/domdfcoding
		$ conda config --add channels http://conda.anaconda.org/conda-forge

	* Then install

	.. code-block:: bash

		$ conda install mathematical

.. end installation
