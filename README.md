# cryptocollector

A simple python module to collect trades from cryptocurrency exchanges.

Supported exchanges are:
    * Coinbase
    * Bitmex

## Getting Started

Install requirements.

### Prerequisites

This module is requires SQL Server to be setup with the database solution available [here]().

### Installing

Clone this repository and run:

```
    python3 setup.py
```

### Usage

To connect to a websocket run:

```
    python3 run_forever.py <name of exchange>
```

The script will run in an endless loop and will reconnect in case of any trouble.

## Authors

* **Brian Esiobu** - *Initial work* - [besiobu](https://github.com/besiobu)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details