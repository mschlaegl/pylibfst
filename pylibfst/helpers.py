# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

from _libfstapi import ffi, lib

def string(val):
    """Converts ffi cdata to python string"""
    if val == ffi.NULL:
        return ""
    return ffi.string(val).decode("UTF-8")


def get_scopes_signals(fst):
    """Iterate the hierarchy (using fstReaderIterateHierRewind and
    fstReaderIterateHier) and return a list containing all scopes names
    and a dictionary containing all signal names with corresponding handles"""

    scopes = []
    signals = {}
    cur_scope = ""
    last_scopes = []

    lib.fstReaderIterateHierRewind(fst)
    while True:
        fstHier = lib.fstReaderIterateHier(fst)
        if fstHier == ffi.NULL:
            break

        if fstHier.htyp == lib.FST_HT_SCOPE:
            last_scopes.append(cur_scope)

            # add new scope
            if cur_scope != "":
                cur_scope += "."
            cur_scope += string(fstHier.u.scope.name)
            scopes.append(cur_scope)

        elif fstHier.htyp == lib.FST_HT_UPSCOPE:
            # restore last scope
            cur_scope = last_scopes.pop()

        elif fstHier.htyp == lib.FST_HT_VAR:
            # add new variable with handle
            var_name = (cur_scope + "." + string(fstHier.u.var.name))
            signals[var_name] = fstHier.u.var.handle

        elif fstHier.htyp == lib.FST_HT_ATTRBEGIN:
            # ignored
            pass
        elif fstHier.htyp == lib.FST_HT_ATTREND:
            # ignored
            pass
        elif fstHier.htyp == lib.FST_HT_TREEBEGIN:
            # ignored
            pass
        elif fstHier.htyp == lib.FST_HT_TREEEND:
            # ignored
            pass
        else:
            print("Invalid htyp in hierarchy" + str(fstHier.htyp))
            return (None, None)

    return (scopes, signals)
