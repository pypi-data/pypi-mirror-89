#!/usr/bin/env python

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='autotracer',
    version='0.0.2',
    description='Runs a code tracer in simple Python scripts for educational purposes',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Andrew Kurauchi',
    author_email='andrewtnk@insper.edu.br',
    url='https://github.com/toshikurauchi/autotracer',
    packages=['autotracer'],
    scripts=['auto_tracer.py'],
    license="MIT",
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
