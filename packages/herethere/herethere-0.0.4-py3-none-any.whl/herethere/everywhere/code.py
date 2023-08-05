"""herethere.everywhere.code"""
from code import InteractiveInterpreter
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from typing import Dict, Optional, TextIO


def runcode(
    code: str,
    stdout: Optional[TextIO] = None,
    stderr: Optional[TextIO] = None,
    namespace: Optional[Dict] = None,
) -> Optional[str]:
    """Execute a code."""
    should_return_value = stdout is None

    if should_return_value:
        stdout = StringIO()

    if stderr is None:
        stderr = stdout

    if namespace is None:
        namespace = {}

    with redirect_stderr(stderr):
        with redirect_stdout(stdout):
            InteractiveInterpreter(locals=namespace).runcode(code)

    if should_return_value:
        if stderr == stdout:
            return stdout.getvalue()
        return "\n".join([stderr.getvalue(), stdout.getvalue()])
    return None
