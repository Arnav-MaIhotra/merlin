import pandas as pd
import yfinance as yf
import time

csv_file = "nasdaq_screener.csv"
data = pd.read_csv(csv_file)[["Symbol", "Industry"]]

ratios = {}

ticker_count = {}

c = 0

for i in data.T:
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

    c += 1

    if c % 250 == 0:
        print(c*100/len(data))
        time.sleep(120)

for i in ratios:
    ratios[i] /= ticker_count[i]

df = pd.DataFrame({"Industry":ratios.keys(), "P/E Ratio":ratios.values()})

df.to_csv("industry_pe_averages.csv", index=False)