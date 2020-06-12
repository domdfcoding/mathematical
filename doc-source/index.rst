=====================
mathematical
=====================

.. start short_desc

**Mathematical tools for Python**

.. end short_desc

Includes tools for calculating mean, median and standard deviation of rows in data frames, detection of outliers, and statistical calculations

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 

.. |docs| image:: https://img.shields.io/readthedocs/mathematical/latest?logo=read-the-docs
	:target: https://mathematical.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/mathematical/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/mathematical
	:alt: Travis Build Status

.. |requires| image:: https://requires.io/github/domdfcoding/mathematical/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/mathematical/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://shields.io/coveralls/github/domdfcoding/mathematical/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/mathematical?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/mathematical?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/mathematical
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/mathematical
	:target: https://pypi.org/project/mathematical/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/mathematical?logo=anaconda
	:alt: Conda - Package Version
	:target: https://anaconda.org/domdfcoding/mathematical

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/mathematical?label=conda%7Cplatform
	:alt: Conda - Platform
	:target: https://anaconda.org/domdfcoding/mathematical

.. |license| image:: https://img.shields.io/github/license/domdfcoding/mathematical
	:alt: License
	:target: https://github.com/domdfcoding/mathematical/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/mathematical
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/mathematical/v0.1.11
	:target: https://github.com/domdfcoding/mathematical/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/mathematical
	:target: https://github.com/domdfcoding/mathematical/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields

Installation
----------------

.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			pip install mathematical

	.. tab:: from Anaconda

		First add the required channels

		.. prompt:: bash

			conda config --add channels http://conda.anaconda.org/domdfcoding
			conda config --add channels http://conda.anaconda.org/conda-forge

		Then install

		.. prompt:: bash

			conda install mathematical

	.. tab:: from GitHub

		.. prompt:: bash

			pip install git+https://github.com//mathematical@master

.. end installation

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	docs
	Source
	Building


.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/mathematical>`__

.. end links