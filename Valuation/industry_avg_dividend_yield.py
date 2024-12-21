import pandas as pd
import yfinance as yf
import time

csv_file = "nasdaq_screener.csv"
data = pd.read_csv(csv_file)[["Symbol", "Industry"]]

yields = {}

ticker_count = {}

c = 0

for i in data.T:
    industry = data.T[i]["Industry"]
    symbol = data.T[i]["Symbol"]

    try:

        stock = yf.Ticker(symbol)
        dividend_yield = stock.info.get('dividendYield')

        if dividend_yield:
            dividend_yield = float(dividend_yield)
        else:
            continue

        if industry not in yields:
            yields[industry] = 0
        if industry not in ticker_count:
            ticker_count[industry] = 0

        yields[industry] += dividend_yield
        ticker_count[industry] += 1
    
    except:
        None

    c += 1

    if c % 250 == 0:
        time.sleep(120)

for i in yields:
    yields[i] /= ticker_count[i]

df = pd.DataFrame({"Industry":yields.keys(), "P/E yield":yields.values()})

df.to_csv("industry_dividend_yield_averages.csv", index=False)