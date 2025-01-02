import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


base_currency = 'EUR'
quote_currency = 'USD'

url = f'https://www.alphavantage.co/query'
params = {
    'function': 'FX_DAILY',
    'from_symbol': base_currency,
    'to_symbol': quote_currency,
    'apikey': API_KEY,
    'outputsize': 'full'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'Time Series FX (Daily)' in data:
        time_series = data['Time Series FX (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close'
        })
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        df.to_csv('forex_data.csv')
        print("Data saved to 'forex_data.csv'")
    else:
        print("Error: No data found.")
else:
    print(f"Error: Unable to fetch data. Status code {response.status_code}")