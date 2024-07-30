"""Handle test measurements."""
from influxdb import InfluxDBClient
from datetime import datetime


def insert_test_measurement(client: InfluxDBClient):
    """Insert the test measurements.

    TODO: Write this as an insert function, accessible via CLI.

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
