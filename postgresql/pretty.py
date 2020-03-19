#! /usr/bin/env python

import lldb

def pretty(valobj, internal_dict):
    expr = 'pretty_format_node_dump(nodeToString({0}))'.format(valobj.GetName())
    pretty_dump = lldb.frame.EvaluateExpression(expr).GetSummary()
    return pretty_dump.replace('\\n', '\n')


def _pretty_type(debugger, typeName):
    #debugger.HandleCommand('type summary add --category Postgres --python-function pretty.pretty {0}'.format(typeName))
    debugger.HandleCommand('type summary add --python-function pretty.pretty {0}'.format(typeName))


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('type category enable Postgres')
    _pretty_type(debugger, 'PlannerInfo')
    _pretty_type(debugger, 'Path')
    _pretty_type(debugger, 'List')
    pass
