import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from datetime import datetime, timedelta

end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

end_date = (datetime.now()-timedelta(days=365*4)).strftime('%Y-%m-%d')
start_date = (datetime.now()-timedelta(days=365*5)).strftime('%Y-%m-%d')

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

def filter_delisted_tickers(tickers):
    valid_tickers = []
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).fast_info
            if data['lastPrice'] is not None:
                valid_tickers.append(ticker)
        except Exception as e:
            print(f"Skipping {ticker}: {e}")
    return valid_tickers


stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)
tickers = get_tickers(tickerss)

data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"].dropna(axis=1, how="all")

returns = data.pct_change(fill_method=None).dropna()

mean_returns = returns.mean()
cov_matrix = returns.cov().fillna(0)

def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

num_assets = len(data.columns)
constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]
bounds = tuple((0, 1) for _ in range(num_assets))

initial_weights = np.array(num_assets * [1.0 / num_assets])

result = minimize(portfolio_volatility, initial_weights, args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=constraints)

optimized_weights = result.x

final_tickers = []

for ticker, weight in zip(data.columns, optimized_weights):
    try:
        price = yf.Ticker(ticker).fast_info["lastPrice"]
        shares = 1000000*weight//price
        final_tickers.append([ticker, shares, price])
    except:
        None

with open("stock_allocations_1m_4y.csv", "w") as file:
    for i in final_tickers:
        file.write(f"{i}\n")