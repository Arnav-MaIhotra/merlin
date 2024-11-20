import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_risk_free_rate():
    treasury_data = yf.Ticker("^IRX").history(period="1d")
    risk_free_rate = treasury_data['Close'].iloc[-1] / 100
    return risk_free_rate

def get_tickers(tickers):
    return [str(ticker) for ticker in tickers if isinstance(ticker, str) and ticker]

def get_sharpe_ratios(stock_list, risk_free_rate=0.01):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    data = yf.download(stock_list, start=start_date, end=end_date)['Adj Close']

    data = data.dropna(axis=1)

    daily_returns = data.pct_change().dropna()

    mean_daily_return = daily_returns.mean()
    std_dev_daily_return = daily_returns.std()

    annualized_return = mean_daily_return * 252
    annualized_std_dev = std_dev_daily_return * np.sqrt(252)

    risk_free_rate = get_risk_free_rate()
    
    sharpe_ratios = (annualized_return - risk_free_rate) / annualized_std_dev

    sharpe_ratios_df = pd.DataFrame(sharpe_ratios, columns=['Sharpe Ratio'])
    sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=False, inplace=True)
    
    sharpe_ratios_df.to_csv('sharpe_ratios.csv')

stocks = pd.read_csv("nasdaq_screener.csv")

tickerss = list(stocks["Symbol"].values)
tickers = get_tickers(tickerss)

get_sharpe_ratios(tickers)