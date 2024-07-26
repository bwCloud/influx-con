"""Manage the library content."""
from typing import Dict


def print_library(lib_cmds: Dict[str, str]):
    """Nice presenting of all entries in the library.

    Args:
        lib_cmds: List of commands.

    """
    for lib_cmd in lib_cmds:
        print(
            "{0:02.0f}:  {1}".format(
                lib_cmd['id'],
                lib_cmd['description']
            )
        )
        print(f"{lib_cmd['cmd']}")
        print()


def get_library_command(
    lib_cmds: Dict[str, str],
    lib_id: int
) -> str:
    """Identify the library entry.

    Args:
        lib_cmds: List of commands.
        lib_id: Target command id.

    Returns: Target command.

    """
    cmd = None
    for lib_cmd in lib_cmds:
        if lib_cmd['id'] == lib_id:
            cmd = lib_cmd['cmd']

    return cmd
