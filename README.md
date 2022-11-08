# Flask Binance Bybit

This is a Flask webhook app for Binance and Bybit both Spot and Futures. The app is created with Python and the Flask microframework. It provides users with a graphical interface to view data from the trades Database.


## Features

* Webhook system for Binance Futures and Bybit
* Multiple take profits
* Web UI that logs the traded that take place or are open at the moment with PNL

## Requirements

* You will also need to generate an API key for the Binance and Bybit exchanges.
* You will need to have a Postgres database setup and the Python libraries installed:
> Python 3.6+
> Flask
> psycopg2
> binance-python
> bybit

## Installation

1. Clone the repo
2. Setup the database
3. Install the requirements

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python3 app.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
