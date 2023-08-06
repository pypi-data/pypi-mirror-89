#!/usr/bin/env python
import os
import sys

import setuptools

descr = """Line Integral Convolution Algorithms to plot 2D vector fields."""

with open("README.md", "r") as fh:
    long_description = fh.read()


DISTNAME = "licplot"
DESCRIPTION = "LIC plotting algorithm."
MAINTAINER = "Alexander Lelidis"
MAINTAINER_EMAIL = "alex.lexus.info@gmail.com"

URL = "https://github.com/alexus37/licplot"
DOWNLOAD_URL = "https://pypi.org/project/licplot"
LICENSE = "BSD"
PACKAGE_NAME = "licplot"


class get_numpy_include(object):
    """Defer numpy.get_include() until after numpy is installed."""

    def __str__(self):
        import numpy

        return numpy.get_include()


# Call the setup function
if __name__ == "__main__":
    setuptools.setup(
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
        ext_modules=[
            setuptools.Extension(
                "licplot.lic_internal",
                sources=["licplot/lic_internal.pyx"],
                include_dirs=[get_numpy_include()]
                # compiler_directives={"language_level": "3"}
            )
        ],
        version="1.0.5",
        setup_requires=[
            # Setuptools 18.0 properly handles Cython extensions.
            "setuptools>=18.0",
            "cython",
            "numpy",
        ],
        install_requires=[
            "numpy",
            "cython",
            "matplotlib",
        ],
        python_requires=">=3.0",
    )
