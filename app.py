from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
from datetime import datetime, timedelta
from utils import workingdays as wd
from utils.patterns import candlestick_patterns as patterns
from utils.patterns_and_desc import pattern_details as pdesc
from scan import scan, scan_all, get_proj_path
import os

app = Flask(__name__)


@app.route("/")
def index():
    pattern = request.args.get("pattern", None)

    stocks = scan(pattern) if pattern else scan_all()
    return render_template(
        "index.html",
        candlestick_patterns=patterns,
        stocks=stocks,
        pattern_details=pdesc,
        pattern=pattern,
    )


# run daily to get last 10 days of data
@app.route("/daily")
def snapshot():
    with open(os.path.join(get_proj_path(), "datasets/watching.csv"), "r") as f:
        stocks = f.read().splitlines()
        for stock in stocks:
            symbol = stock.split(",")[0]

            df = yf.download(
                symbol,
                start=wd.n_business_days_earlier(10).strftime("%Y-%m-%d"),
                end=datetime.today().strftime("%Y-%m-%d"),
            )

            quote_path = os.path.join(get_proj_path(), "datasets/daily")
            df.to_csv(f"{quote_path}/{symbol}.csv")

    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
