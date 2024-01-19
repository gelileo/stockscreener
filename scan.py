import os, csv
import pandas as pd
import talib
from utils.patterns import candlestick_patterns as patterns

# groups
ticker_groups = [("spy", "S&P 500"), ("watching", "Watching List")]
code_to_group = {key: value for key, value in ticker_groups}
group_To_code = {value: key for key, value in ticker_groups}


def get_proj_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_group_symbols(group):
    ticker_dir = os.path.join(get_proj_path(), "datasets/tickers")
    ticker_file = f"{group_To_code[group]}.csv"
    symbols = []
    with open(os.path.join(ticker_dir, ticker_file), "r") as f:
        for row in csv.reader(f):
            symbols.append(row[0])
    return symbols


def initialize_stocks(group=None, ticker_names=None):
    stocks = {}

    ticker_list = None
    if ticker_names:
        ticker_list = [item.strip() for item in ticker_names.split(",")]

    ticker_dir = os.path.join(get_proj_path(), "datasets/tickers")
    # List all CSV files in the directory
    ticker_files = [f for f in os.listdir(ticker_dir) if f.endswith(".csv")]
    for ticker_file in ticker_files:
        if ticker_list:
            with open(os.path.join(ticker_dir, ticker_file), "r") as f:
                for row in csv.reader(f):
                    if row[0] in ticker_list:
                        stocks[row[0]] = {"company": row[1]}
        else:
            if group and ticker_file != f"{group_To_code[group]}.csv":
                continue

            with open(os.path.join(ticker_dir, ticker_file), "r") as f:
                for row in csv.reader(f):
                    stocks[row[0]] = {"company": row[1]}

    return stocks


def scan_all(group=None, ticker_names=None):
    stocks = initialize_stocks(group, ticker_names)
    tickers = list(stocks.keys())
    for pattern in patterns.keys():
        stocks = match_pattern(pattern, stocks)

    # remove stocks with no patterns
    filtered_stocks = {ticker: info for ticker, info in stocks.items() if len(info) > 1}

    return (filtered_stocks, tickers)


def scan(pattern=None, group=None, ticker_names=None):
    stocks = initialize_stocks(group, ticker_names)
    tickers = list(stocks.keys())
    if pattern:
        match_pattern(pattern, stocks)
        return (stocks, tickers)
    else:
        return (stocks, tickers)


def match_pattern(pattern, stocks):
    quote_path = os.path.join(get_proj_path(), "datasets/daily")
    datafiles = os.listdir(quote_path)
    pattern_function = getattr(talib, pattern)
    found = False
    for datafile in datafiles:
        df = pd.read_csv(f"{quote_path}/{datafile}").tail(14)  # the last 14 days
        symbol = datafile.split(".")[0]
        try:
            if symbol not in stocks:
                continue

            pattern_result = pattern_function(
                df["Open"], df["High"], df["Low"], df["Close"]
            )
            if (
                len(pattern_result.tail(1).values) > 0
            ):  # tail(1) returns the last row, i.e. the latest day
                last = pattern_result.tail(1).values[0]
                if last > 0:
                    stocks[symbol][pattern] = "bullish"
                    found = True
                    print(f"{datafile} triggered {pattern} at {last}")
                elif last < 0:
                    stocks[symbol][pattern] = "bearish"
                # else:
                #     stocks[symbol][pattern] = None
        except Exception as e:
            print(f"Failed on {datafile}")

    if not found:
        print(f"No symbols found for pattern {pattern}")

    print(stocks)
    return stocks
