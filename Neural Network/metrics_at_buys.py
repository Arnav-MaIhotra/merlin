import pandas as pd
import yfinance as yf

stock = yf.Ticker("AAPL")
dividend_yield = stock.info

print(dividend_yield)