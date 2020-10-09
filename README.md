# cryptocollector

<img src="https://raw.githubusercontent.com/besiobu/cryptocollector/main/img/xbt_report.PNG" width="517" height="353" />

A simple python module to collect trades from cryptocurrency exchanges.

## Features
* Write messages directly to database.
* In case write fails - save message to `json`.
* Each message is timestamped before inserting into database.
* Automatic reconnecting to websockets.
* Logging.

## Supported exchanges
* Coinbase
* Bitmex

## Prerequisites

This module is requires SQL Server to be setup with the database solution available [here]().

## Getting Started

Clone this repository and run:

```
    python3 setup.py
```

## Installing

Install requirements:
```
    pip3 install -r requirements.txt
```

## Usage

To connect to a websocket run:

```
    python3 run_forever.py <name of exchange>
```

The script will run in an endless loop and will reconnect in case of any trouble.

## Authors

* **Brian Esiobu** - *Initial work* - [besiobu](https://github.com/besiobu)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details