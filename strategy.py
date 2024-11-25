import pandas as pd
import vectorbt as vbt
import random
import time

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)

tickers = get_tickers(tickerss)

count = 0

test_tickers = pd.read_csv("sharpe_ratios.csv").get("Ticker").values[0:20]

print(test_tickers)

total_tickers = 20

for i in test_tickers:

    price = vbt.YFData.download(i, start="2023-11-25", end="2024-11-25").get("Close")

    ma1 = vbt.MA.run(price, 10)
    ma2 = vbt.MA.run(price, 50)
    RSI = vbt.RSI.run(price)

    entries = ma1.ma_crossed_above(ma2) & RSI.rsi_above(50)
    exits = ma2.ma_crossed_above(ma1)

    pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)
    if pf.total_profit() == 0:
        print("BLANK")
        continue
    count += pf.total_profit()
    print(i, pf.total_profit())

print(count/total_tickers)