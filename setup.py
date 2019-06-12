from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="mathematical",
	version="0.1.0",
    author='Dominic Davis-Foster',
	author_email="dominic@davis-foster.co.uk",
	packages=find_packages(),
	license="OSI Approved :: GNU General Public License v3 (GPLv3)",
	url="https://github.com/domdfcoding/mathematical",
	description='Mathematical tools for python',
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta",
    ],
	install_requires=[
		"scipy >= 1.3.0",
		"numpy >= 1.16.0",
	],
)
