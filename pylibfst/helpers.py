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


def get_signal_name_by_handle(signals, handle):
    """Returns the first matching signal name from the
    given signals dictionary for the given handle"""
    return list(signals.keys())[list(signals.values()).index(handle)]



def fstReaderIterBlocks(fst,
        value_change_callback,
        user_callback_data = None, vcdhandle = None):
    """Wrapped version of fstReaderIterBlocks. Allows the use of any
    normal python function as callback (with slight overhead)"""

    if vcdhandle is None:
        vcdhandle = ffi.NULL

    # wrap python callbacks and callback data
    data = ffi.new_handle(
            (
                value_change_callback,
                None,
                user_callback_data
            )
    )

    # call with wrapper
    return lib.fstReaderIterBlocks(
            fst,
            lib.pylibfst_wrapped_value_change_callback,
            data,
            vcdhandle)


def fstReaderIterBlocks2(fst,
        value_change_callback, value_change_callback_varlen,
        user_callback_data = None, vcdhandle = None):
    """Wrapped version of fstReaderIterBlocks2. Allows the use of any
    normal python function as callback (with slight overhead)"""

    if vcdhandle is None:
        vcdhandle = ffi.NULL

    # wrap python callbacks and callback data
    data = ffi.new_handle(
            (
                value_change_callback,
                value_change_callback_varlen,
                user_callback_data
            )
    )

    # call with wrapper
    return lib.fstReaderIterBlocks2(
            fst,
            lib.pylibfst_wrapped_value_change_callback,
            lib.pylibfst_wrapped_value_change_callback_varlen,
            data,
            vcdhandle)


@ffi.def_extern()
def pylibfst_wrapped_value_change_callback(data, time, facidx, value):
    """INTERNAL USE ONLY!
    Callback wrapper for fstReaderIterBlocks and fstReaderIterBlocks2.
    Unwraps python function and data and calls the python function with data"""

    # unwrap python callback and data
    data = ffi.from_handle(data)
    # call wrapped callback
    data[0](data[2], time, facidx, value)


@ffi.def_extern()
def pylibfst_wrapped_value_change_callback_varlen(data, time, facidx, value, length):
    """INTERNAL USE ONLY!
    Callback wrapper for fstReaderIterBlocks2.
    Unwraps python function and data and calls the python function with data"""

    # unwrap python callback and data
    data = ffi.from_handle(data)
    # call wrapped callback
    data[1](data[2], time, facidx, value, length)
