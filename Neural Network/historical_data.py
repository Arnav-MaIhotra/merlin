import yfinance as yf
import pandas as pd
import os
import sys
import time

stocks = pd.read_csv(r"C:\Users\maskenzi\Documents\merlin\nasdaq_screener.csv")

tickers = list(stocks["Symbol"].values)[5250:]

for i in range(len(tickers)):
    tickers[i] = str(tickers[i])

count = 0

for ticker in tickers:

    if "/" in ticker or "^" in ticker:
        count += 1
        continue

    data = yf.download(ticker, interval="1wk", end="2024-01-01")

    data.to_csv(r"C:\Users\maskenzi\Documents\merlin\Neural Network\stock_data/{}.csv".format(ticker))

    count += 1
    if count % 250 == 0:

        print(count*100/len(tickers))
        time.sleep(120)