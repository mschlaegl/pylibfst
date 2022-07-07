# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

import sys
import pylibfst

# cffi style callbacks

@pylibfst.ffi.def_extern()
def pylibfst_value_change_callback(
        user_callback_data_pointer,
        time, facidx, value):

    print("value_change_callback " + str(time) + " " + str(facidx)
            + " " + pylibfst.helpers.get_signal_name_by_handle(signals, facidx)
            + " " + pylibfst.helpers.string(value))


@pylibfst.ffi.def_extern()
def pylibfst_value_change_callback_varlen(
        user_callback_data_pointer,
        time, facidx, value, length):

    print("value_change_callback_varlen " + str(time) + " " + str(facidx)
            + " " + pylibfst.helpers.get_signal_name_by_handle(signals, facidx)
            + " " + pylibfst.helpers.string(value) + " " + str(length))




if len(sys.argv) != 2:
    print("IterBlocks_callback (pylibfst example) (C) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>\n")
    print("Usage: " + sys.argv[0] + " <fstfile>\n")
    print("Example: " + sys.argv[0] + " counter.fst\n")
    sys.exit(1)
filename = sys.argv[1]

fst = pylibfst.lib.fstReaderOpen(filename.encode("UTF-8"))
if fst == pylibfst.ffi.NULL:
    print("Unable to open file '" + filename + "'!");
    sys.exit(1)



(scopes, signals) = pylibfst.get_scopes_signals(fst)

pylibfst.lib.fstReaderSetFacProcessMaskAll(fst)

print("fstReaderIterBlocks")
ret = pylibfst.lib.fstReaderIterBlocks(
        fst,
        pylibfst.lib.pylibfst_value_change_callback,
        pylibfst.ffi.NULL,
        pylibfst.ffi.NULL)
print("ret " + str(ret))

print("fstReaderIterBlocks2")
ret = pylibfst.lib.fstReaderIterBlocks2(
        fst,
        pylibfst.lib.pylibfst_value_change_callback,
        pylibfst.lib.pylibfst_value_change_callback_varlen,
        pylibfst.ffi.NULL,
        pylibfst.ffi.NULL)
print("ret " + str(ret))

pylibfst.lib.fstReaderClose(fst)
print("done")
