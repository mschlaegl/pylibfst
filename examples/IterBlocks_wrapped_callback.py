# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

import sys
import pylibfst

# pythonic callbacks

def value_change_callback(data, time, facidx, value):

    print("value_change_callback " + str(data)
            + " " + str(time) + " " + str(facidx)
            + " " + pylibfst.helpers.get_signal_name_by_handle(signals, facidx)
            + " " + pylibfst.helpers.string(value))


def value_change_callback_varlen(data, time, facidx, value, length):

    print("value_change_callback_varlen " + str(data)
            + " " + str(time) + " " + str(facidx)
            + " " + pylibfst.helpers.get_signal_name_by_handle(signals, facidx)
            + " " + pylibfst.helpers.string(value) + " " + str(length))




if len(sys.argv) != 2:
    print("IterBlocks_wrapped_callback (pylibfst example) (C) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>\n")
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
ret = pylibfst.helpers.fstReaderIterBlocks(
        fst,
        value_change_callback,
        "My_Test_Data") # can be any python object
print("ret " + str(ret))

print("fstReaderIterBlocks2")
ret = pylibfst.helpers.fstReaderIterBlocks2(
        fst,
        value_change_callback,
        value_change_callback_varlen,
        "My_Test_Data") # can be any python object
print("ret " + str(ret))

pylibfst.lib.fstReaderClose(fst)

print("done")
