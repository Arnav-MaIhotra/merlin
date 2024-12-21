import yfinance as yf
import pandas as pd

stocks = pd.read_csv("nasdaq_screener.csv")

tickers = list(stocks["Symbol"].values)

yields = {}

maxt = len(tickers)

i = 0

for ticker in tickers:
    i += 1
    if i%100 == 0:
        print(100*i/maxt, "%")
    try:
        comp = yf.Ticker(ticker).info
        if not comp:
            continue
        if not comp.get("dividendYield"):
            continue
        yields[ticker] = comp.get("dividendYield")
    except:
        continue


with open("dividends.csv", "w") as file:
    for item in sorted(yields.items(), key=lambda x: x[1]):
        file.write(f"{item}\n")