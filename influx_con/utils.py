"""Utils for the tool."""
from sys import exit
from yaml import safe_load
from typing import List


def handle_errors(
    msg: str,
    code: int
) -> str:
    """Handle the error.

    Args:
        msg: Error message.
        code: Error code.
    """
    print(msg)
    exit(code)


def read_yaml(path: str) -> dict:
    """Read the yaml file.

    Args:
        path: Path to the file.

    Returns:
        File content.
    """
    try:
        with open(
            path,
            'r'
        ) as reader:
            content = safe_load(reader)
    except FileNotFoundError as err:
        handle_errors(
            err,
            10
        )

    return content


def parse_config(path: str) -> List[dict]:
    """Parse in the config file the connection and profiles settings.

    Args:
        path: Path to the file.

    Returns:
        The connection properties.
        The user profiles.
    """
    config = read_yaml(path)

    return config['connection'], config['profiles']


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
