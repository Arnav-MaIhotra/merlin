import yfinance as yf
import pandas as pd

stocks = pd.read_csv("nasdaq_screener.csv").sample(50)

tickers = list(stocks["Symbol"].values)

data = yf.download(tickers, "2014-01-01", "2024-01-01")

print(data["Adj Close"].to_csv("e.csv"))