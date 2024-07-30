"""Utils for the tool."""
from sys import exit
from yaml import safe_load
from typing import List, Dict


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


def get_user_profile(
    profiles: Dict[str, str],
    target: str
) -> Dict[str, str]:
    """Get the user properties.

    Args:
        profiles: List of profiles.
        target: Name of profile.

    Returns: The settings for the target profile.

    """
    user = profiles.get(target, None)
    if user is None:
        err_msg = f"Error: The profile '{target}' is not defined. " \
                f'Supported is: {list(profiles.keys())}.'
        handle_errors(
            err_msg,
            10
        )

    return user
