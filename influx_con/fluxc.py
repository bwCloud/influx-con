"""CLI application for influx-con."""
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from textwrap import dedent
from pathlib import Path
from time import sleep

from influx_con.utils import \
    parse_config, \
    get_user_profile
from influx_con.library import \
    quick_library, \
    show_library
from influx_con.test_measurement import \
    insert_test_measurement
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
    library_path = Path.home().joinpath('./.local/share/fluxc/library.yml')
    parser.add_argument(
        '--library',
        metavar='PATH',
        action='store',
        default=library_path,
        help=f"""
            Path to the statement library file.
            Def. is '{library_path}'.
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


def modus_test(args: Namespace):
    """Execute a set of test querys.

    Args:
        args: Settings.

    """
    config_file = args.config
    library_file = args.library

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

    quick_library(
        library_file,
        config_file,
        'reader',
        1
    )
    quick_library(
        library_file,
        config_file,
        'reader',
        2
    )

    # == Clean up ==
    quick_library(
        library_file,
        config_file,
        'admin',
        3
    )


def modus_lib(args: Namespace):
    """Execute an query form the library or show the library.

    Args:
        args: Settings and the library entry ID.

    """
    config_file = args.config
    library_file = args.library
    profile = args.profile
    lib_id = args.id

    # Only print library and exit
    if lib_id is None:
        show_library(library_file)
        return

    # Run library command
    quick_library(
        library_file,
        config_file,
        profile,
        lib_id
    )


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
