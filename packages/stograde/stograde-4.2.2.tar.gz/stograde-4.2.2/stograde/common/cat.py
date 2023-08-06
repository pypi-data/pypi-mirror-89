from typing import Tuple

from .run_status import RunStatus


def cat(filename: str, *, hide_contents: bool = False) -> Tuple[RunStatus, str]:
    """Return the contents of a file. Replaces the `cat` command.

    This function took about ~148 time units per call, while
    run(['cat']) needed ~4688 time units.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            return RunStatus.SUCCESS, infile.read() if not hide_contents else ''
    except FileNotFoundError:
        return RunStatus.FILE_NOT_FOUND, ''
