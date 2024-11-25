import vectorbt as vbt
from datetime import datetime, timedelta
import math
import pandas as pd
import time

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)

tickers = get_tickers(tickerss)

risk_free_rate = 0.04

end_date = datetime.now() - timedelta(days=365)
start_date = end_date - timedelta(days=365)

sharpes = {}

count = 0

for ticker in tickers:

    count += 1
    if count % 250 == 0:
        time.sleep(120)

    try:

        data = vbt.YFData.download(ticker, start=start_date, end=end_date).get("Close")

        daily_returns = data.pct_change().dropna()

        excess_returns = daily_returns - (risk_free_rate / 252)
        sharpe_ratio = excess_returns.mean() * math.sqrt(252) / excess_returns.std()

        sharpes[ticker] = sharpe_ratio
    
    except:
        None

print(sharpes)

sharpe_ratios_df = pd.DataFrame(list(sharpes.items()), columns=["Ticker", "Sharpe Ratio"])

sharpe_ratios_df.to_csv("sharpe_ratios_vectorbt_1y.csv", index=False)