import sys
import imp
from collections import namedtuple
from autotracer import mock
from copy import deepcopy

# This could be interesting to replace a lot of code: https://github.com/ionelmc/python-hunter
# This could also be useful: https://medium.com/tenable-techblog/remapping-python-opcodes-67d79586bfd5
# This documentation may be useful: https://docs.python.org/3/library/inspect.html
'''
TODO
Do not go inside functions that were not defined in the module
'''

TraceData = namedtuple('TraceData', 'line_i,line,name_dicts,call_line_i,retval,stdout')

TRACED_MODULE_NAME = 'traced_user_module'


class AutoTracer:
    def __init__(self):
        self._reset()
        self.module = None

    def _reset(self):
        self._started = False
        self.stack = []
        self.trace = []
        self.prev_line = None
        self.prev_lineno = 0
        self.src = None
        self.src_lines = []
        self.mock_builtins = mock.MockBuiltins()

    def _build_name_dicts(self, frame, *, name_dicts=None, functions=None):
        if functions is None:
            functions = []
        f_name = frame.f_code.co_name
        if name_dicts:
            name_dicts = {
                '{0},{1}'.format(f_name, k): deepcopy(v)
                for k, v in name_dicts.items()
            }
        else:
            name_dicts = {}
        frame_dict = {}

        # TODO Maybe this is better: https://github.com/pgbovine/OnlinePythonTutor/blob/master/v5-unity/pg_logger.py#L431
        variables = frame.f_code.co_varnames + frame.f_code.co_names
        for v in variables:
            if v in frame.f_locals:
                value = frame.f_locals[v]
                if callable(value):
                    functions.append(value)
                else:
                    frame_dict[v] = deepcopy(value)
        name_dicts[f_name] = frame_dict

        # We should stop when we reach a frame that is not traced
        if frame.f_back and frame.f_back.f_globals.get('__name__') == TRACED_MODULE_NAME:
            return self._build_name_dicts(frame.f_back,
                                          name_dicts=name_dicts,
                                          functions=functions)
        return name_dicts, functions

    def _is_def(self, f_name, cur_line):
        return cur_line and 'def ' in cur_line and f_name not in cur_line

    def _trace(self, frame, event, arg):
        with self.mock_builtins.temp_deactivate():
            f_name = frame.f_code.co_name
            lineno = frame.f_lineno
            module_name = frame.f_globals.get('__name__')

            if not self._started:
                if event == 'call' and module_name == TRACED_MODULE_NAME:
                    self._started = True
                return self._trace

            # Ignore other modules (change this if additional modules need to be traced)
            if module_name != TRACED_MODULE_NAME:
                return self._trace

            try:
                call_line_i = self.stack[-1][0] - 1
            except IndexError:
                call_line_i = None
            try:
                cur_line = self.src_lines[lineno - 1]
            except IndexError:
                cur_line = None

            print(lineno, cur_line, event, f_name, module_name)
            name_dicts, functions = self._build_name_dicts(frame)
            if self._is_def(f_name, cur_line):
                return self._trace
            if event == 'line':
                if self.prev_line:
                    self.trace.append(
                        TraceData(self.prev_lineno - 1, self.prev_line, name_dicts,
                                call_line_i, None, self.mock_builtins.outputs))
                self.prev_line = cur_line
                self.prev_lineno = lineno
            elif event == 'call' and not self._is_def(f_name, cur_line):
                if self.prev_line:
                    self.stack.append((self.prev_lineno, self.prev_line))
                    if self.trace:
                        last = self.trace[-1]
                        self.trace.append(
                            TraceData(self.prev_lineno - 1, self.prev_line,
                                    *last[2:]))
                self.trace.append(
                    TraceData(
                    lineno - 1, cur_line, name_dicts,
                    self.prev_lineno - 1, None,
                    self.mock_builtins.outputs
                ))
                self.prev_line = None
                self.prev_lineno = 0
            elif event == 'return':
                if self.prev_line:
                    self.trace.append(
                        TraceData(self.prev_lineno - 1, self.prev_line, name_dicts,
                                call_line_i, arg, self.mock_builtins.outputs))
                try:
                    self.prev_lineno, self.prev_line = self.stack.pop()
                except IndexError:
                    self.prev_lineno, self.prev_line = 0, None

            return self._trace

    def trace_file(self, filename, stdin=None):
        with open(filename) as f:
            return self.trace_str(f.read(), stdin=stdin)

    def trace_str(self, src_str, stdin=None):
        self.src = src_str
        self.src_lines = src_str.split('\n')

        self.mock_builtins.stdin = stdin
        with self.mock_builtins:
            self.module = imp.new_module(TRACED_MODULE_NAME)
            exec(self.src, self.module.__dict__)

        return self.module

    def __enter__(self):
        self._reset()
        sys.settrace(self._trace)
        return self

    def __exit__(self, *args, **kwargs):
        sys.settrace(None)
