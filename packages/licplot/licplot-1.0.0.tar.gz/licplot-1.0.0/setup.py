#!/usr/bin/env python
import os
import sys

import setuptools
from numpy.distutils.core import setup
from Cython.Build import cythonize

descr = """Line Integral Convolution Algorithms to plot 2D vector fields."""
requirements = open("requirements.txt").read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()


DISTNAME = "licplot"
DESCRIPTION = "LIC plotting algorithm."
MAINTAINER = "Alexander Lelidis"
MAINTAINER_EMAIL = "alex.lexus.info@gmail.com"
# TODO: fix url
URL = "https://pypi.org/project/licplot"
DOWNLOAD_URL = URL
LICENSE = "BSD"
PACKAGE_NAME = "licplot"


# Call the setup function
if __name__ == "__main__":
    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        include_package_data=True,
        zip_safe=False,
        ext_modules=cythonize(
            "licplot/lic_internal.pyx", compiler_directives={"language_level": "3"}
        ),
        version="1.0.0",
        install_requires=requirements,
        python_requires=">=3.0",
    )
