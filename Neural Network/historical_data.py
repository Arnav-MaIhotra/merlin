import yfinance as yf
import pandas as pd

stocks = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\nasdaq_screener.csv")

tickers = list(stocks["Symbol"].values)

for i in range(len(tickers)):
    tickers[i] = str(tickers[i])

data = yf.download(tickers, "2014-01-01", "2024-01-01")

print(data["Adj Close"].to_csv("Neural Network/10y_data.csv"))