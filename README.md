# cryptocollector

![image](https://github.com/besiobu/cryptocollector/blob/main/img/xbt_report.PNG)

A simple python module to collect trades from cryptocurrency exchanges.

## Features
* Persistance: Messages are written directly to staging area in database.
* Exception handling - if a write fails the message from exchange is saved to `json`.
* Timestamping: Each message is timestamped by the script before persisting to database.
* Run forever: Script to automatically reconnect to exchange websocket.
* Logging: Handled by Python's logging module.

## Supported exchanges
* Coinbase
* Bitmex
* `more coming`

## Prerequisites

This module is requires SQL Server to be setup with the database solution available [here](https://github.com/besiobu/cryptocollector_db).

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