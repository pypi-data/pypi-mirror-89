# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as file:
    README = file.read()

with open("LICENSE") as file:
    LICENSE = file.read()

setup(
    name = "FlightRadarAPI",
    version = "1.0.0",
    description = "API for FlightRadar24",
    long_description = README,
    author = "Jean Loui Bernard Silva de Jesus",
    url = "https://github.com/JeanExtreme002/Flightradar24",
    license = LICENSE,
    keywords = "flightradar24 api",
    packages = find_packages(exclude = ("tests", "docs")),
    install_requires = ["Brotli", "requests"]
)
