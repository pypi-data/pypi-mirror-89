import builtins
from collections import namedtuple
from io import StringIO
import sys


OutputLine = namedtuple('OutputLine', 'std_output,user_input')


class MockFunction:
    def __init__(self):
        self.calls = 0
        self.args = []
        self.kwargs = []

    def __call__(self, *args, **kwargs):
        self.args.append(args)
        self.kwargs.append(kwargs)
        self.calls += 1


class MockPrint(MockFunction):
    def __init__(self, python_print, outputs):
        super().__init__()
        self.printed = []
        self.python_print = python_print
        self.outputs = outputs

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        line = ' '.join([str(arg) for arg in args])  # There is probably a more reliable way to do this...
        self.outputs.append(OutputLine(line, None))
        self.printed.append(line)
        self.python_print(*args, ** kwargs)


class MockInput(MockFunction):
    def __init__(self, python_input, outputs):
        super().__init__()
        self.python_input = python_input
        self.outputs = outputs

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        line = ''
        if args:
            line = args[0]
        retval = self.python_input(*args, **kwargs)
        self.outputs.append(OutputLine(line, retval))
        return retval


class MockBuiltins():
    class TempDeactivateMock:
        def __init__(self, mock):
            self.mock = mock

        def __enter__(self):
            self.mock.__exit__()
            return self.mock

        def __exit__(self, *args, **kwargs):
            self.mock.__enter__()

    def __init__(self):
        self._outputs = []
        self.python_print = builtins.print
        self.mock_print = MockPrint(self.python_print, self._outputs)
        self.python_input = builtins.input
        self.mock_input = MockInput(self.python_input, self._outputs)
        self.stdin = ''
        self.py_stdin = sys.stdin

    def __enter__(self):
        # Replace builtins
        builtins.print = self.mock_print
        builtins.input = self.mock_input

        if self.stdin:
            sys.stdin = StringIO(self.stdin)
        return self

    def __exit__(self, *args, **kwargs):
        # Restore builtins
        builtins.print = self.python_print
        builtins.input = self.python_input
        sys.stdin = self.py_stdin

    def temp_deactivate(self):
        return MockBuiltins.TempDeactivateMock(self)

    @property
    def outputs(self):
        # Create copy
        return [e for e in self._outputs]
