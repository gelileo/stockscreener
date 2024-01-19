from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
from utils.patterns import candlestick_patterns as patterns
from utils.patterns_and_desc import pattern_details as pdesc
from scan import scan, scan_all, get_proj_path, ticker_groups as groups
from quotes import get_quote
import os
import json

app = Flask(__name__)


@app.route("/status")
def status():
    return "Running"


@app.route("/")
def index():
    pattern = request.args.get("pattern", None)
    group = request.args.get("ticker_group", None)
    ticketnames = request.args.get("ticker_names", None)
    (stocks, tickers) = (
        scan(pattern, group, ticketnames) if pattern else scan_all(group, ticketnames)
    )
    ticker_names_json = json.dumps(tickers)
    return render_template(
        "index.html",
        candlestick_patterns=patterns,
        stocks=stocks,
        pattern_details=pdesc,
        pattern=pattern,
        ticker_groups=[group[1] for group in groups],
        ticker_names=ticker_names_json,
    )


# run daily to get last 10 days of data
@app.route("/daily")
def snapshot():
    ticker_dir = os.path.join(get_proj_path(), "datasets/tickers")

    # List all CSV files in the directory
    ticker_files = [f for f in os.listdir(ticker_dir) if f.endswith(".csv")]

    # Initialize an empty set for stock symbols
    symbols = set()

    for ticker_file in ticker_files:
        with open(os.path.join(ticker_dir, ticker_file), "r") as f:
            stocks = f.read().splitlines()
            for stock in stocks:
                symbol = stock.split(",")[0]
                symbols.add(symbol)

    for symbol in symbols:
        quote_path = os.path.join(get_proj_path(), "datasets/daily")
        get_quote(symbol, quote_path)

    return f"updated quotes for {len(symbols)} stocks!"


if __name__ == "__main__":
    app.run(debug=True)
