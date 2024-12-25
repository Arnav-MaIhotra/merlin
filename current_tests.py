import finnhub
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

print(yf.download("AAPL", start="2012-03-06", end="2012-03-08")["Close"].iloc[0].values[0])