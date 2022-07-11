# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pylibfst",
    version="0.1.0", # semantic versioning (Major.Minor.Patch)
    author="Manfred SCHLAEGL, fst C implementation: Tony Bybell",
    author_email="manfred.schlaegl@gmx.at",
    description="Handling of Fast Signal Traces (fst) in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mschlaegl/pylibfst",
    keywords="fst, eda, gtkwave, vcd",
    classifiers=[
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Unix",
        #"Operating System :: MacOS :: MacOS X",        # Untested
        #"Operating System :: Microsoft :: Windows",    # Untested
    ],
    packages=find_packages(),
    setup_requires=["cffi>=1.15.0"],
    cffi_modules=["pylibfst/libfstapi_build.py:ffibuilder"],
    install_requires=["cffi>=1.15.0"],
)
