# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

print find_packages()
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="gridworld_plot",
    version="0.1.0",
    description="A package for plotting q functions (and related) for gridworlds.",
    license="MIT",
    author="John Salvatier",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
