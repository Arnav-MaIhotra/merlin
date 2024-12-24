import finnhub
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

symbol = "TXRH"

try:
    financials = finnhub_client.company_basic_financials(symbol, 'all')

    eps_data = financials.get('series', {}).get('quarterly', {}).get('eps', [])

    if eps_data:
        print("Historical EPS Data:")
        for entry in eps_data:
            print(f"Year: {entry['period']}, EPS: {entry['v']}")
    else:
        print("No EPS data available for this stock.")
except Exception as e:
    print(f"Error fetching data: {e}")