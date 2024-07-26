"""CLI application for influx-con."""
from typing import Dict
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from textwrap import dedent
from pathlib import Path
from time import sleep

from influx_con.utils import handle_errors, parse_config, parse_library
from influx_con.library import \
    print_library, get_library_command
from influx_con.test_measurement import \
    insert_test_measurement, \
    print_test_measurement, \
    drop_test_measurement
from influx_con.idbccclient import \
    open_connection, \
    run_select_query, \
    print_measurements


def parse_args() -> Namespace:
    """Parse arguments.

    Returns: Parsed args.

    """
    parser = ArgumentParser(
        prog='my-script',
        formatter_class=RawDescriptionHelpFormatter,
        description=dedent("""\
            Client for connecting to the InfluxDB.
        """),
        epilog=dedent("""\
            Example:
              - # fluxc test
              - # fluxc run --profile reader 'select values form telegraf;'
        """)
    )
    subparser = parser.add_subparsers(
        dest='sub_parser',  # Use this to address the selected sub-parser
        help='The modus to choose.'
    )

    # == General ==
    config_path = Path.home().joinpath('./.fluxc.conf')
    parser.add_argument(
        '--config',
        metavar='PATH',
        action='store',
        default=config_path,
        help=f"""
            Path to the influx config file.
            Def. is '{config_path}'.
        """
    )
    parser.add_argument(
        '--profile',
        metavar='NAME',
        action='store',
        default='admin',
        help="""
            The profile refered in the CONFIG file.
            Def. is 'admin'.
        """
    )

    # == Test ==
    # parser_test
    _ = subparser.add_parser(
        'test',
        help='Run test statements against a test measurement.'
    )

    # == Library ==
    parser_lib = subparser.add_parser(
        'lib',
        help='Show or run statements from the library.'
    )
    library_path = Path.home().joinpath('./.local/share/fluxc/library.yml')
    parser_lib.add_argument(
        '--library',
        metavar='PATH',
        action='store',
        default=library_path,
        help=f"""
            Path to the statement library file.
            Def. is '{library_path}'.
        """
    )
    parser_lib.add_argument(
        'id',
        metavar='ID',
        action='store',
        default=None,
        nargs='?',
        type=int,
        help="""
            The ID of the library statement to execute.
            If not given, the library is printed.
        """
    )

    # == Run ==
    parser_run = subparser.add_parser(
        'run',
        help='Run a InfluxQL command.'
    )
    parser_run.add_argument(
        'influxql',
        metavar='INFLUXQL',
        action='extend',
        nargs='*',
        help="The InfluxQL statement to execute."
    )

    args = parser.parse_args()
    return args


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


def modus_test(args: Namespace):
    """Execute a set of test querys.

    Args:
        args: Settings.

    """
    config_file = args.config

    # Parse config
    cfg_conn, cfg_profiles = parse_config(config_file)

    # == Write data ==
    write_user = get_user_profile(
        cfg_profiles,
        'writer'
    )
    # Open write connection to database
    write_client = open_connection(
        cfg_conn['host'],
        cfg_conn['port'],
        write_user['name'],
        write_user['pw'],
        cfg_conn['database'],
        ssl=cfg_conn['ssl'],
    )
    # Create some entries and present them
    num_entrie = 3
    for e in range(num_entrie):
        insert_test_measurement(write_client)
        # Some time gap between the entries
        if e != num_entrie - 1:
            sleep(1)

    # == Read data ==
    read_user = get_user_profile(
        cfg_profiles,
        'reader'
    )
    # Open read connection to database
    read_client = open_connection(
        cfg_conn['host'],
        cfg_conn['port'],
        read_user['name'],
        read_user['pw'],
        cfg_conn['database'],
        ssl=cfg_conn['ssl'],
    )
    print_test_measurement(read_client)

    # == Clean up ==
    admin_user = get_user_profile(
        cfg_profiles,
        'admin'
    )
    # Open admin connection to database
    admin_client = open_connection(
        cfg_conn['host'],
        cfg_conn['port'],
        admin_user['name'],
        admin_user['pw'],
        cfg_conn['database'],
        ssl=cfg_conn['ssl'],
    )
    drop_test_measurement(admin_client)


def modus_lib(args: Namespace):
    """Execute an query form the library or show the library.

    Args:
        args: Settings and the library entry ID.

    """
    config_file = args.config
    profile = args.profile
    library_file = args.library
    lib_id = args.id

    lib_cmds = parse_library(library_file)

    # Default case
    if lib_id is None:
        print_library(lib_cmds)
        return

    # Parse config
    cfg_conn, cfg_user = parse_config(config_file)

    # Open connection to database
    user = cfg_user[profile]
    client = open_connection(
        cfg_conn['host'],
        cfg_conn['port'],
        user['name'],
        user['pw'],
        cfg_conn['database'],
        ssl=cfg_conn['ssl'],
    )

    cmd = get_library_command(
        lib_cmds,
        lib_id
    )

    # Run query
    result = run_select_query(
        client,
        cmd
    )
    print_measurements(result)


def modus_run(args: Namespace):
    """Execute a query and print the result.

    Args:
        args: Settings and the query to execute.

    """
    config_file = args.config
    cmd = args.influxql
    profile = args.profile

    # Parse config
    cfg_conn, cfg_user = parse_config(config_file)

    # Open connection to database
    user = cfg_user[profile]
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
    print_measurements(result)


def main():
    """Start scripts."""
    parsed_args = parse_args()

    if parsed_args.sub_parser == 'test':
        modus_test(parsed_args)
    if parsed_args.sub_parser == 'run':
        modus_run(parsed_args)
    if parsed_args.sub_parser == 'lib':
        modus_lib(parsed_args)


# == start ==
if __name__ == "__main__":
    main()
