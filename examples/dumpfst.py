# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

import sys
import pylibfst

def printi(indent, *args):
    for i in range(indent):
        print("  ", end="")
    print("+ ", end="")
    print(*args)


def dumpHierachryEntryScope(indent, fstHier):
    printi(indent, "Scope:")
    indent += 1
    printi(indent, "Type:          " + str(fstHier.u.scope.typ))
    printi(indent, "Name:          " + pylibfst.helpers.string(fstHier.u.scope.name))
    printi(indent, "Component:     " + str(pylibfst.helpers.string(fstHier.u.scope.component)))
    return indent


def dumpHierachryEntryVar(indent, fstHier):
    printi(indent, "Var:")
    indent += 1
    printi(indent, "Type:          " + str(fstHier.u.var.typ))
    printi(indent, "Name:          " + pylibfst.helpers.string(fstHier.u.var.name))
    printi(indent, "Direction:     " + str(fstHier.u.var.direction))
    printi(indent, "SVT Workspace: " + str(fstHier.u.var.svt_workspace))
    printi(indent, "SDT Workspace: " + str(fstHier.u.var.sdt_workspace))
    printi(indent, "SXT Workspace: " + str(fstHier.u.var.sxt_workspace))
    printi(indent, "Length:        " + str(fstHier.u.var.length))
    printi(indent, "fstHandle:     " + str(fstHier.u.var.handle))
    printi(indent, "is_alias:      " + str(fstHier.u.var.is_alias))
    indent -= 1
    return indent


def dumpHierachryEntryAttrBegin(indent, fstHier):
    printi(indent, "AttrBegin:")
    indent += 1
    printi(indent, "Type:          " + str(fstHier.u.attr.typ))
    printi(indent, "Sub Type:      " + str(fstHier.u.attr.subtyp))
    printi(indent, "Name:          " + pylibfst.helpers.string(fstHier.u.attr.name))
    printi(indent, "Arg:           " + str(fstHier.u.attr.arg))
    printi(indent, "Arg from Name: " + str(fstHier.u.attr.arg_from_name))
    return indent


def dumpHierachryEntryTreeBegin(indent, fstHier):
    indent += 1
    print(" + TreeBegin: Not Implemented")
    return indent


def dumpHierachyEntry(indent, fstHier):

    if fstHier.htyp == pylibfst.lib.FST_HT_SCOPE:
        indent = dumpHierachryEntryScope(indent, fstHier)

    elif fstHier.htyp == pylibfst.lib.FST_HT_UPSCOPE:
        indent -= 1

    elif fstHier.htyp == pylibfst.lib.FST_HT_VAR:
        indent = dumpHierachryEntryVar(indent, fstHier)

    elif fstHier.htyp == pylibfst.lib.FST_HT_ATTRBEGIN:
        indent = dumpHierachryEntryAttrBegin(indent, fstHier)

    elif fstHier.htyp == pylibfst.lib.FST_HT_ATTREND:
        indent -= 1

    elif fstHier.htyp == pylibfst.lib.FST_HT_TREEBEGIN:
        indent = dumpHierachryEntryTreeBegin(indent, fstHier)

    elif fstHier.htyp == pylibfst.lib.FST_HT_TREEEND:
        indent -= 1

    else:
        print("Invalid htyp " + str(fstHier.htyp))

    return indent


def dumpHierachy(fst):

    print("DUMP HIRARCHY: ")
    indent = 0
    pylibfst.lib.fstReaderIterateHierRewind(fst)

    while True:
        fstHier = pylibfst.lib.fstReaderIterateHier(fst)
        if fstHier == pylibfst.ffi.NULL:
            break
        indent = dumpHierachyEntry(indent, fstHier)


def dump(fst):

    verStr = pylibfst.lib.fstReaderGetVersionString(fst)
    print("Version String:           " + pylibfst.helpers.string(verStr))

    date = pylibfst.lib.fstReaderGetDateString(fst)
    print("Date String:              " + pylibfst.helpers.string(date))

    fileType = pylibfst.lib.fstReaderGetFileType(fst)
    print("File Type:                " + str(fileType))

    varCount = pylibfst.lib.fstReaderGetVarCount(fst)
    print("Var Count:                " + str(varCount))

    scopeCount = pylibfst.lib.fstReaderGetScopeCount(fst)
    print("Scope Count:              " + str(scopeCount))

    aliasCount = pylibfst.lib.fstReaderGetAliasCount(fst)
    print("Alias Count:              " + str(aliasCount))

    startTime = pylibfst.lib.fstReaderGetStartTime(fst)
    endTime = pylibfst.lib.fstReaderGetEndTime(fst)
    print("Start Time:               " + str(startTime))
    print("End Time:                 " + str(endTime))

    timeScale = pylibfst.lib.fstReaderGetTimescale(fst)
    print("Time Scale:               " + str(timeScale))

    timeZero = pylibfst.lib.fstReaderGetTimezero(fst)
    print("Time Zero:                " + str(timeZero))

    valChSecCnt = pylibfst.lib.fstReaderGetValueChangeSectionCount(fst)
    print("Value Change Section Cnt: " + str(valChSecCnt))

    dumpHierachy(fst)



def dump_signals(fst, signals):

    # get timestamps of all signal changes
    pylibfst.lib.fstReaderSetFacProcessMaskAll(fst)
    timestamps = pylibfst.lib.fstReaderGetTimestamps(fst)

    for signal in signals:
        print("'" + str(signal) + "'; ", end="")
    print()

    buf = pylibfst.ffi.new("char[256]")
    for ts in range(timestamps.nvals):
        time = timestamps.val[ts]
        print("{: >5d}; ".format(time), end="")
        for signal in signals:
            handle = signals[signal]
            val = pylibfst.helpers.string(pylibfst.lib.fstReaderGetValueFromHandleAtTime(fst, time, handle, buf))
            print(str(val) + "; ", end="")
        print()

    pylibfst.lib.fstReaderFreeTimestamps(timestamps)

if len(sys.argv) != 2:
    print("dumpfst (pylibfst example) (C) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>\n")
    print("Usage: " + sys.argv[0] + " <fstfile>\n")
    print("Example: " + sys.argv[0] + " counter.fst\n")
    sys.exit(1)
filename = sys.argv[1]

fst = pylibfst.lib.fstReaderOpen(filename.encode("UTF-8"))
if fst == pylibfst.ffi.NULL:
    print("Unable to open file '" + filename + "'!");
    sys.exit(1)

dump(fst)
print()

(scopes, signals) = pylibfst.get_scopes_signals(fst)
print("scopes:  " + str(scopes))
print("signals: " + str(signals))
print()

dump_signals(fst, signals)
print()

pylibfst.lib.fstReaderClose(fst)
print("done")
