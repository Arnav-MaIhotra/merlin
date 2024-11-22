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

time.sleep(300)

price = vbt.YFData.download("NVDA").get("Close")

ma1 = vbt.MA.run(price, 10)
ma2 = vbt.MA.run(price, 50)
RSI = vbt.RSI.run(price)

entries = ma1.ma_crossed_above(ma2) & RSI.rsi_above(50)
exits = ma2.ma_crossed_above(ma1)

pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)

#SHARPES

print(pf.stats())

"""

total_tickers = 0

for j in range(10):

    try:

        test_tickers = random.sample(tickers, 10)

        for i in test_tickers:

            if total_tickers % 250 == 0:
                time.sleep(120)

            price = vbt.YFData.download(i, start="2020-11-20", end="2024-11-20").get("Close")

            ma1 = vbt.MA.run(price, 10)
            ma2 = vbt.MA.run(price, 50)
            ma3 = vbt.MA.run(price, 200)
            RSI = vbt.RSI.run(price)

            entries = ma1.ma_crossed_above(ma2/2) & RSI.rsi_above(50)# & ma2.ma_crossed_above(ma3)
            exits = ma2.ma_crossed_above(ma1)

            pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)
            if pf.total_profit() == 0:
                print("BLANK")
                continue
            count += pf.total_profit()
            print(i, pf.total_profit())
            total_tickers += 1
    except:
        None

print(count/total_tickers)

"""