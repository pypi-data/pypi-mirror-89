#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name="Zgoubi metadata",
	version="0.1",
	author="Sam Tygier",
	author_email="sam@tygier.co.uk",
	description="Metadata for building software to interact with Zgoubi",
	url="https://github.com/PyZgoubi/zgoubi-metadata",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=find_packages(),
	include_package_data=True,
	install_requires=["PyYAML>=5.3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
