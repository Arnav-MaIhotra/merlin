import vectorbt as vbt
import pandas as pd
import random
import numpy as np

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)

tickers = random.sample(get_tickers(tickerss), 100)

profits = []

for i in tickers:

    price = vbt.YFData.download(i, start="2023-12-04", end="2024-11-29").get("Close")

    ma1 = vbt.MA.run(price, 5)
    ma2 = vbt.MA.run(price, 10)
    RSI = vbt.RSI.run(price)

    entries = ma1.ma_crossed_above(ma2) & RSI.rsi_below(30)
    exits = ma2.ma_crossed_above(ma1) & RSI.rsi_above(70)

    pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)

    print(pf.total_profit())
    profits.append(pf.total_profit())

print(np.average([i for i in profits if i != 0]))