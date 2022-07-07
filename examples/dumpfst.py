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
    printi(indent, "Name:          " + str(pylibfst.ffi.string(fstHier.u.scope.name)))
    printi(indent, "Name Len:      " + str(fstHier.u.scope.name_length))
    printi(indent, "Component:     " + str(pylibfst.ffi.string(fstHier.u.scope.component)))
    printi(indent, "Component Len: " + str(fstHier.u.scope.component_length))
    return indent


def dumpHierachryEntryVar(indent, fstHier):
    printi(indent, "Var:")
    indent += 1
    printi(indent, "Type:          " + str(fstHier.u.var.typ))
    printi(indent, "Name:          " + str(pylibfst.ffi.string(fstHier.u.var.name)))
    printi(indent, "Name Len:      " + str(fstHier.u.var.name_length))
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
    printi(indent, "Name:          " + str(pylibfst.ffi.string(fstHier.u.attr.name)))
    printi(indent, "Name Len:      " + str(fstHier.u.attr.name_length))
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
    print("Version String:    " + str(pylibfst.ffi.string(verStr)))

    date = pylibfst.lib.fstReaderGetDateString(fst)
    print("Date String:       " + str(pylibfst.ffi.string(date)))

    fileType = pylibfst.lib.fstReaderGetFileType(fst)
    print("File Type:         " + str(fileType))

    varCount = pylibfst.lib.fstReaderGetVarCount(fst)
    print("Var Count:         " + str(varCount))

    scopeCount = pylibfst.lib.fstReaderGetScopeCount(fst)
    print("Scope Count:       " + str(scopeCount))

    aliasCount = pylibfst.lib.fstReaderGetAliasCount(fst)
    print("Alias Count:       " + str(aliasCount))

    startTime = pylibfst.lib.fstReaderGetStartTime(fst)
    endTime = pylibfst.lib.fstReaderGetEndTime(fst)
    print("Start Time:        " + str(startTime))
    print("End Time:          " + str(endTime))

    timeScale = pylibfst.lib.fstReaderGetTimescale(fst)
    print("Time Scale:        " + str(timeScale))

    timeZero = pylibfst.lib.fstReaderGetTimezero(fst)
    print("Time Zero:         " + str(timeZero))

    valChSecCnt = pylibfst.lib.fstReaderGetValueChangeSectionCount(fst)
    print("V Change Sec Cnt:  " + str(valChSecCnt))

    #void            fstReaderClrFacProcessMask(void *ctx, fstHandle facidx);
    #void            fstReaderClrFacProcessMaskAll(void *ctx);
    #const char *    fstReaderGetCurrentFlatScope(void *ctx);
    #void *          fstReaderGetCurrentScopeUserInfo(void *ctx);
    #int             fstReaderGetCurrentScopeLen(void *ctx);
    #int             fstReaderGetDoubleEndianMatchState(void *ctx);
    #uint64_t        fstReaderGetDumpActivityChangeTime(void *ctx, uint32_t idx);
    #unsigned char   fstReaderGetDumpActivityChangeValue(void *ctx, uint32_t idx);
    #int             fstReaderGetFacProcessMask(void *ctx, fstHandle facidx);
    #int             fstReaderGetFseekFailed(void *ctx);
    #fstHandle       fstReaderGetMaxHandle(void *ctx);
    #uint64_t        fstReaderGetMemoryUsedByWriter(void *ctx);
    #uint32_t        fstReaderGetNumberDumpActivityChanges(void *ctx);
    #int             fstReaderIterBlocks(void *ctx,
    #                        void (*value_change_callback)(void *user_callback_data_pointer, uint64_t time, fstHandle facidx, const unsigned char *value),
    #                        void *user_callback_data_pointer, FILE *vcdhandle);
    #int             fstReaderIterBlocks2(void *ctx,
    #                        void (*value_change_callback)(void *user_callback_data_pointer, uint64_t time, fstHandle facidx, const unsigned char *value),
    #                        void (*value_change_callback_varlen)(void *user_callback_data_pointer, uint64_t time, fstHandle facidx, const unsigned char *value, uint32_t len),
    #                        void *user_callback_data_pointer, FILE *vcdhandle);
    #void            fstReaderIterBlocksSetNativeDoublesOnCallback(void *ctx, int enable);
    #void *          fstReaderOpenForUtilitiesOnly(void);
    #const char *    fstReaderPopScope(void *ctx);
    #int             fstReaderProcessHier(void *ctx, FILE *vcdhandle);
    #const char *    fstReaderPushScope(void *ctx, const char *nam, void *user_info);
    #void            fstReaderResetScope(void *ctx);
    #void            fstReaderSetFacProcessMask(void *ctx, fstHandle facidx);
    #void            fstReaderSetFacProcessMaskAll(void *ctx);
    #void            fstReaderSetLimitTimeRange(void *ctx, uint64_t start_time, uint64_t end_time);
    #void            fstReaderSetUnlimitedTimeRange(void *ctx);
    #void            fstReaderSetVcdExtensions(void *ctx, int enable);

    dumpHierachy(fst)



def dump_signals(fst):
    (_, signals) = pylibfst.get_scopes_signals(fst)
    for signal in signals:
        print(str(signal) + " ", end="")
    print()

    buf = pylibfst.ffi.new("char[256]")
    for time in range(pylibfst.lib.fstReaderGetStartTime(fst), pylibfst.lib.fstReaderGetEndTime(fst)):
        print('{: >5d}'.format(time) + " ", end="")
        for signal in signals:
            handle = signals[signal]
            val = pylibfst.ffi.string(pylibfst.lib.fstReaderGetValueFromHandleAtTime(fst, time, handle, buf))
            val = val.decode('UTF-8')
            #val = int(val)
            print(str(val) + " ", end="")
        print()



fst = pylibfst.lib.fstReaderOpen(b"counter.fst")
if fst == pylibfst.ffi.NULL:
    print("unable to open file!");
    sys.exit(1)

dump(fst)

(scopes, signals) = pylibfst.get_scopes_signals(fst)
print("scopes  " + str(scopes))
print("signals " + str(signals))

dump_signals(fst)

pylibfst.lib.fstReaderClose(fst)

print("done")
