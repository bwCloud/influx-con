"""Manage the library content."""
from typing import Dict, List, Tuple
from influx_con.utils import read_yaml
from influx_con.idbccclient import quick_query


def parse_library(path: str) -> List[dict]:
    """Parse the statements in the library.

    Args:
        path: Path to the file.

    Returns: The statements
    """
    library = read_yaml(path)
    library = library['commands']
    for e, lib_cmd in enumerate(library):
        lib_cmd['id'] = e + 1
    return library


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
) -> Tuple[str, str]:
    """Identify the library entry.

    Args:
        lib_cmds: List of commands.
        lib_id: Target command id.

    Returns: Target caption and command.

    """
    cmd = None
    for lib_cmd in lib_cmds:
        if lib_cmd['id'] == lib_id:
            cmd = lib_cmd['cmd']
            caption = lib_cmd['description']

    return caption, cmd


def show_library(
    library_file: str
):
    """Print the library commands.

    Args:
        library_file: Path to the library file.

    """
    lib_cmds = parse_library(library_file)
    print_library(lib_cmds)


def quick_library(
    library_file: str,
    config_file: str,
    profile: str,
    lib_id: int,
):
    """Run a library command.

    Args:
        library_file: Path to library file.
        config_file: Patht to config file.
        profile: Name of the profile.
        lib_id: ID of the library command.

    """
    lib_cmds = parse_library(library_file)

    caption, cmd = get_library_command(
        lib_cmds,
        lib_id
    )
    quick_query(
        config_file,
        profile,
        cmd,
        caption=caption
    )
