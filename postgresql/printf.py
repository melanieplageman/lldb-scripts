import functools
import re

import lldb


def read_string(sbval, length = 1048576):
    if not sbval.TypeIsPointerType():
        hint = sbval.type.name
        raise TypeError("can't read string from a non-pointer value of type (%s)" % hint)

    e = lldb.SBError()
    address = sbval.GetValueAsUnsigned(e)
    if e.fail:
        raise TypeError("can't coerce value [%s] into an address" % sbval)

    process = sbval.GetProcess()
    if not process:
        raise ValueError("can't read string from a value unassociated with a process")

    e = lldb.SBError()
    string = process.ReadCStringFromMemory(address, length, e)
    if e.fail:
        hint = e.description
        raise ValueError("can't read string from address %s: %s" % (hex(address), hint))
    return string


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f printf.printf printf')


def printf(debugger, command, result, internal_dict):
    output = None
    try:
        output = actual_printf(debugger, command, result, internal_dict)
    except Exception as e:
        # Remove redundant instances of "error: " from the beginning of the
        # error string. Because result.SetError will prepend "error: " to
        # its argument we ensure that we provide a string without "error: "
        # at the beginning. In addition result.SetError will append a
        # newline to its argument so strip redundant newlines from the end.
        result.SetError(re.sub(r"^(?:error: )+", "", str(e)).rstrip())
    return output


def actual_printf(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    if not target:
        result.SetError("no selected target available")
        return

    val = target.EvaluateExpression(command)
    e = val.error
    if e.fail:
        raise ValueError(e.description)

    print(read_string(val))
