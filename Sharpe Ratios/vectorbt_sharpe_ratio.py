import vectorbt as vbt
from datetime import datetime, timedelta
import math
import time
import pandas as pd

def get_trading_days(start_date, end_date, holidays=[]):
    all_dates = pd.date_range(start=start_date, end=end_date, freq='B')
    trading_days = all_dates.difference(pd.to_datetime(holidays))
    return len(trading_days)

def next_business_day(start_date=None):
    next_day = start_date + timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    return next_day

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

stocks = pd.read_csv("nasdaq_screener.csv")
tickerss = list(stocks["Symbol"].values)
tickers = get_tickers(tickerss)

risk_free_rate = 0.04

end_date = datetime.now() - timedelta(days=365)
start_date = end_date - timedelta(days=365)

start_date = next_business_day(start_date)
end_date = next_business_day(end_date)

print(start_date, end_date)

sharpes = {}

count = 0

for ticker in tickers:
    count += 1
    if count % 250 == 0:
        time.sleep(120)

    try:
        data = vbt.YFData.download(ticker, start=start_date, end=end_date).get("Close")
        
        if len(data) < 250 or len(data) > 252:
            continue

        daily_returns = data.pct_change().dropna()
        excess_returns = daily_returns - (risk_free_rate / 252)
        sharpe_ratio = excess_returns.mean() * math.sqrt(252) / excess_returns.std()

        sharpes[ticker] = sharpe_ratio
    
    except:
        None

print(sharpes)

sharpes = dict(sorted(sharpes.items(), key=lambda item: item[1], reverse=True))

sharpe_ratios_df = pd.DataFrame(list(sharpes.items()), columns=["Ticker", "Sharpe Ratio"])
sharpe_ratios_df.to_csv("sharpe_ratios_vectorbt_1y.csv", index=False)