import os, csv
import pandas as pd
import talib
from utils.patterns import candlestick_patterns as patterns


def get_proj_path():
    return os.path.dirname(os.path.abspath(__file__))


def initialize_stocks():
    stocks = {}
    stock_path = os.path.join(get_proj_path(), "datasets/spy.csv")
    with open(stock_path, "r") as f:
        for row in csv.reader(f):
            stocks[row[0]] = {"company": row[1]}

    stock_path = os.path.join(get_proj_path(), "datasets/watching.csv")
    with open(stock_path, "r") as f:
        for row in csv.reader(f):
            stocks[row[0]] = {"company": row[1]}

    return stocks


def scan_all():
    stocks = initialize_stocks()

    for pattern in patterns.keys():
        stocks = match_pattern(pattern, stocks)

    # remove stocks with no patterns
    filtered_stocks = {ticker: info for ticker, info in stocks.items() if len(info) > 1}

    return filtered_stocks


def scan(pattern=None):
    stocks = initialize_stocks()
    if pattern:
        match_pattern(pattern, stocks)
        return stocks
    else:
        return stocks


def match_pattern(pattern, stocks):
    quote_path = os.path.join(get_proj_path(), "datasets/daily")
    datafiles = os.listdir(quote_path)
    pattern_function = getattr(talib, pattern)
    found = False
    for datafile in datafiles:
        df = pd.read_csv(f"{quote_path}/{datafile}").tail(10)
        symbol = datafile.split(".")[0]
        try:
            if symbol not in stocks:
                continue

            pattern_result = pattern_function(
                df["Open"], df["High"], df["Low"], df["Close"]
            )
            if len(pattern_result.tail(1).values) > 0:
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


sth = {
    "MMM": {"company": "3M Company", "CDLMATCHINGLOW": "bearish"},
    "MSFT": {
        "company": "Microsoft Corp.",
        "CDLENGULFING": "bearish",
        "CDLHIKKAKE": "bullish",
    },
    "MAA": {"company": "Mid-America Apartments"},
    "AMD": {"company": "Advanced Micro Devices Inc", "CDLENGULFING": "bullish"},
    "AAP": {"company": "Advance Auto Parts", "CDLHIKKAKE": "bullish"},
}
