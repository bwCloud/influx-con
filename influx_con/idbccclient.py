"""Mange connection to influx databse."""
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from typing import List, Union


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
