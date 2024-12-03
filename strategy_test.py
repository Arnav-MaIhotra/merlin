import vectorbt as vbt


price = vbt.YFData.download("AAON", start="2023-12-04", end="2024-11-29").get("Close")

pe_ratio = vbt.
RSI = vbt.RSI.run(price)

entries = ma1.ma_crossed_above(ma2) & RSI.rsi_below(30)
exits = ma2.ma_crossed_above(ma1)

pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)

print(pf.total_profit())

print(pf.stats())

pf.plot().show()