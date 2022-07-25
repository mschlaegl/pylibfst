# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

import os
from cffi import FFI

ffibuilder = FFI()

with open(os.path.join(os.path.dirname(__file__), "libfstapi.cdef")) as fp:
    cdef = fp.read()
ffibuilder.cdef(cdef)
ffibuilder.set_source(
    "_libfstapi",
    """
    // the C headers of the library
    #include "fstapi.h"
    #include "fstext.h"
""",
    # fstapi(libfstapi.a) is created by setup.py using
    # cmake and the original CMakeLists.txt of fst
    libraries=["fst/fstapi", "z"],
    include_dirs=["fst"],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
