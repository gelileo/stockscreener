from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import os
from utils import workingdays as wd


# Download quote data for given stock symbol from Yahoo Finance
def get_quote(symbol, quote_path):
    file_path = f"{quote_path}/{symbol}.csv"
    # Determine the start date
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        last_date = pd.to_datetime(existing_df["Date"]).max()
        start_date = last_date + timedelta(days=1)
    else:
        start_date = wd.n_business_days_earlier(10)

    # Download new data if start_date is less than today
    if start_date < datetime.today():
        df = yf.download(
            symbol,
            start=start_date.strftime("%Y-%m-%d"),
            end=datetime.today().strftime("%Y-%m-%d"),
        )

        # Append or write to CSV
        if os.path.exists(file_path):
            df.to_csv(file_path, mode="a", header=False)
        else:
            df.to_csv(file_path)
