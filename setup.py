# -*- coding: utf-8 -*-
import os

from distutils.core import setup

from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="gssync",
    version="2.1.0",
    author="Pierre Hardy",
    author_email="",
    description="Django App to sync GeoNode with GeoServer",
    long_description=(read("README.md")),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
    ],
    license="GPL",
    keywords="geoserver geonode django egis",
    url="https://github.com/phardy-egis/django-geonode-gssync",
    packages=find_packages(),
    dependency_links=["git+https://github.com/phardy-egis/django-geonode-gssync.git#egg=gssync"],
    include_package_data=True,
)
