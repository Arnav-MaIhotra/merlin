import pandas as pd
import vectorbt as vbt
import random
import time
import matplotlib.pyplot as plt

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)

tickers = get_tickers(tickerss)

df = pd.read_csv("sharpe_ratios_vectorbt_1y.csv")

profits = []

indiv_profits = []

total_tickers = 0

for i in df.get("Sharpe Ratio").values:
    if i > 0:
        total_tickers += 1
    else:
        break

test_tickers = df.get("Ticker").values[0:total_tickers]

tickers_downloaded = 0

for i in test_tickers:

    tickers_downloaded += 1

    price = vbt.YFData.download(i, start="2023-12-04", end="2024-11-29").get("Close")

    ma1 = vbt.MA.run(price, 10)
    ma2 = vbt.MA.run(price, 50)
    RSI = vbt.RSI.run(price)

    entries = ma1.ma_crossed_above(ma2) & RSI.rsi_below(30)
    exits = ma2.ma_crossed_above(ma1)

    pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)
    if pf.total_profit() == 0:
        indiv_profits.append("BLANK")
        continue
    indiv_profits.append(pf.total_profit())

    if tickers_downloaded % 250 == 0:
        time.sleep(120)

for j in range(0, 251):

    count = 0

    total_tickers = 0

    for i in df.get("Sharpe Ratio").values:
        if i > j/100:
            total_tickers += 1
        else:
            break

    counted_tickers = 0

    for p in range(total_tickers):
        if indiv_profits[p] == "BLANK":
            continue
        count += indiv_profits[p]
        counted_tickers += 1
    
    profits.append(count/counted_tickers)

values1 = range(0, 251)

values = [x / 100 for x in values1]

plt.plot(values, profits)

plt.show()