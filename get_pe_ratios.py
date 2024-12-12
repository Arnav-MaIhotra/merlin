import pandas as pd
import yfinance as yf
import time

csv_file = "nasdaq_screener.csv"
data = pd.read_csv(csv_file)[["Symbol", "Industry"]]

ratios = {}

ticker_count = {}

for i in data.T:
    if i % 250 == 0:
        time.sleep(120)
    industry = data.T[i]["Industry"]
    symbol = data.T[i]["Symbol"]

    try:

        stock = yf.Ticker(symbol)
        pe_ratio = stock.info.get('trailingPE')

        if pe_ratio:
            pe_ratio = float(pe_ratio)
        else:
            continue

        if industry not in ratios:
            ratios[industry] = 0
        if industry not in ticker_count:
            ticker_count[industry] = 0

        ratios[industry] += pe_ratio
        ticker_count[industry] += 1
    
    except:
        None

for i in ratios:
    ratios[i] /= ticker_count[i]

df = pd.DataFrame({"Industry":ratios.keys(), "P/E Ratio":ratios.values()})

df.to_csv("industry_pe_averages.csv", index=False)