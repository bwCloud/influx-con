"""Handle test measurements."""
from influxdb import InfluxDBClient
from datetime import datetime

from influx_con.idbccclient import run_select_query, print_measurements


def insert_test_measurement(client: InfluxDBClient):
    """Insert the test measurements.

    Args:
        client: Open write connection.

    """
    meas_name = 'test_meas'
    current_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    random_dummy_value1 = datetime.now().strftime('%f')
    meas_entry_1 = [
        {
            "measurement": meas_name,
            "tags": {
                "host": "second_host",
            },
            "time": current_timestamp,
            "fields": {
                "value": random_dummy_value1
            }
        }
    ]
    random_dummy_value2 = datetime.now().strftime('%f')
    meas_entry_2 = [
        {
            "measurement": meas_name,
            "tags": {
                "host": "first_host",
            },
            "time": current_timestamp,
            "fields": {
                "value": random_dummy_value2
            }
        }
    ]

    client.write_points(meas_entry_1)
    client.write_points(meas_entry_2)


def print_test_measurement(client: InfluxDBClient):
    """Read and dump the test measurements.

    Args:
        client: Open read connection.

    """
    meas_name = 'test_meas'

    # Example for getting all values
    cmd = f'select * from {meas_name};'
    result = run_select_query(
        client,
        cmd
    )
    caption1 = f'Result: {meas_name}'
    print_measurements(
        result,
        caption=caption1,
    )

    # Example for filtering by tags
    tag_filter2 = {'host': 'second_host'}
    caption2 = f'Result: {meas_name} for \'second_tag\''
    print_measurements(
        result,
        tag_filter=tag_filter2,
        caption=caption2,
    )


def drop_test_measurement(client: InfluxDBClient):
    """Remove the test measurement.

    Args:
        client: Open admin connection.

    """
    meas_name = 'test_meas'

    cmd = f'DROP MEASUREMENT "{meas_name}";'
    client.query(cmd)
