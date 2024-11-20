import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

add = 0

for y in range(1, 11):

    path = f"sharpe_ratios_{y}y.csv"

    df = pd.read_csv(path)

    returns = []

    for i in range(5, 51):

        tickers = list(df["Ticker"].values[0:i])

        end_date = datetime.today()# - timedelta(days=365*(y-1))
        start_date = end_date - timedelta(days=365*y)

        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

        daily_returns = data.pct_change().dropna()

        num_tickers = len(tickers)
        portfolio_daily_returns = daily_returns.mean(axis=1)

        annual_return = (np.prod(1 + portfolio_daily_returns)) - 1

        returns.append(annual_return)

    add += returns.index(max(returns))

add /= 10

print(add)