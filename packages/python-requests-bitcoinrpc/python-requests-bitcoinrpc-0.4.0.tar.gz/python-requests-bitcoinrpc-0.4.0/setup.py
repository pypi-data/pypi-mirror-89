#!/usr/bin/env python

from setuptools import setup

__version__ = "v0.4.0"

setup(
    name="python-requests-bitcoinrpc",
    version=__version__,
    description="Enhanced version python-bitconrpc using requests sessions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Norman Moeschter-Schenck",
    author_email="<norman.moeschter@gmail.com>",
    maintainer="Norman Moeschter-Schenck",
    maintainer_email="<norman.moeschter@gmail.com>",
    url="https://www.github.com/normoes/python-bitcoinrpc",
    download_url=f"https://github.com/normoes/python-bitcoinrpc/archive/{__version__}.tar.gz",
    packages=["bitcoinrpc"],
    install_requires=["requests>=2.23.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
