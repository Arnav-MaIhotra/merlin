import finnhub
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

