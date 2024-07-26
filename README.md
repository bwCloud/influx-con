InfluxDB Connector Client
===

# Project Overview
Connector for the influxDB.


# Installation Instructions
Run the following commands:

1. `git clone git@gitlab.kit.edu:kit/scc/bwcloud/utils/influx-con.git'
2. `cd influx-con`
3. `pip install .
4. `fluxc -h`


# Usage Guide
Exampels:

- `fluxc --profile reader run 'select value from telegraf;'`
- `fluxc test`
  ```
  Result: test_meas
    00  {'time': '2024-07-11T10:48:56Z', 'host': 'first_host', 'value': '389247'}
    01  {'time': '2024-07-11T10:48:56Z', 'host': 'second_host', 'value': '389231'}
    02  {'time': '2024-07-11T10:48:57Z', 'host': 'first_host', 'value': '429395'}
    03  {'time': '2024-07-11T10:48:57Z', 'host': 'second_host', 'value': '429379'}
    04  {'time': '2024-07-11T10:48:58Z', 'host': 'first_host', 'value': '439929'}
    05  {'time': '2024-07-11T10:48:58Z', 'host': 'second_host', 'value': '439916'}
  Result: test_meas for 'second_tag'
    00  {'time': '2024-07-11T10:48:56Z', 'host': 'second_host', 'value': '389231'}
    01  {'time': '2024-07-11T10:48:57Z', 'host': 'second_host', 'value': '429379'}
    02  {'time': '2024-07-11T10:48:58Z', 'host': 'second_host', 'value': '439916'}
  ```


# Configuration
The default config path is `~/.fluxc.conf`.
An initial configuration can be found in `./fluxc/config/`.

- `ssh`: Set this to 'true', if a TLS-proxy is forwarding the connection to an influxDB.

The default library path is `~/.local/share/fluxc/library.yml`
An basic statements can be found in `./fluxc/library/`.


# Contributing Guidelines
Development setup:

1. `git clone git@gitlab.kit.edu:kit/scc/bwcloud/utils/influx-con.git'
2. `cd influx-con`
3. `pip install -e .[tests]`
4. Code guidelines checking: `make check_code`

