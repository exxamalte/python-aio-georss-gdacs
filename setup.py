"""Setup of aio_georss_gdacs library."""

from setuptools import find_packages, setup

from aio_georss_gdacs.__version__ import __version__

NAME = "aio_georss_gdacs"
AUTHOR = "Malte Franken"
AUTHOR_EMAIL = "coding@subspace.de"
DESCRIPTION = "An async GeoRSS client library for GDACS feeds."
URL = "https://github.com/exxamalte/python-aio-georss-gdacs"

REQUIRES = [
    "aio_georss_client>=0.12",
    "python-dateutil>=2.9.0",
]


with open("README.md") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=__version__,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES,
)
