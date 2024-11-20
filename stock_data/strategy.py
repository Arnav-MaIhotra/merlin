import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

stocks = pd.read_csv("nasdaq_screener.csv")

tickers = list(stocks["Symbol"].values)

count = 0

for i in tickers:
    try:
        count += 1
        if "/" in i or "/" in i or "^" in i:
            continue
        df = yf.download(i, (datetime.today() - timedelta(365)).strftime("%Y-%m-%d"), datetime.today())
        if not df.empty:
            df.to_csv("stock_data/" + i + ".csv")
        
        if count % 250 == 0:
            time.sleep(120)
    except Exception as e:
        print(i, e)
