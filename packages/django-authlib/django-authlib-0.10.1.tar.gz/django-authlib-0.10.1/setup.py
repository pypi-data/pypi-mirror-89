#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="django-authlib",
    version=__import__("authlib").__version__,
    description="Authentication utils for Django",
    long_description=read("README.rst"),
    author="Matthias Kestenholz",
    author_email="mk@feinheit.ch",
    url="http://github.com/matthiask/django-authlib/",
    license="MIT License",
    platforms=["OS Independent"],
    packages=find_packages(exclude=["tests", "testapp"]),
    include_package_data=True,
    install_requires=["requests-oauthlib"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
