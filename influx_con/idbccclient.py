"""Mange connection to influx databse."""
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from typing import List, Union

from influx_con.utils import \
        parse_config, \
        get_user_profile


def open_connection(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str,
    ssl: bool = True,
) -> InfluxDBClient:
    """Open the connection to the database.

    Args:
        host: The host running the database.
        port: The port for accessing the database.
        username: Name of database user.
        password: Password for the database user.
        database: Name of target database.
        ssl: If the conntions is secured via TLS.

    Returns: The connection socket.

    """
    client = InfluxDBClient(
        host,
        port,
        username,
        password,
        database,
        ssl=ssl
    )

    return client


def run_select_query(
    client: InfluxDBClient,
    cmd: Union[List[str], str]
) -> ResultSet:
    """Execute the query and return the result.

    Args:
        client: Connection socket.
        cmd: Command to execute.

    Returns: Command result.

    """
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)
    result = client.query(cmd)

    return result


def print_measurements(
    result: ResultSet,
    tag_filter: dict = None,
    caption: str = None
):
    """Dump a query result.

    Args:
        result: Query result.
        tag_filter: Filter for the result.
        caption: Caption to print for the result.

    """
    if tag_filter is None:
        tag_filter = {}

    if caption is not None:
        print(caption)
    for e, point in enumerate(result.get_points(tags=tag_filter)):
        print('  {0:02.0f}  {1}'.format(e, point))


def quick_query(
    config_file: str,
    profile: str,
    cmd: str,
    **kwargs
):
    """Connect and run a query.

    Args:
        config_file: Patht to config file.
        profile: Profile name.
        cmd: Command to execute.
        kwargs: Options supported by other functions.

    """
    # Parse config
    cfg_conn, cfg_profiles = parse_config(config_file)

    # Open connection to database
    user = get_user_profile(
        cfg_profiles,
        profile
    )
    client = open_connection(
        cfg_conn['host'],
        cfg_conn['port'],
        user['name'],
        user['pw'],
        cfg_conn['database'],
        ssl=cfg_conn['ssl'],
    )

    # Run query
    result = run_select_query(
        client,
        cmd
    )
    print_measurements(
        result,
        **kwargs
    )
