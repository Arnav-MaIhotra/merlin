import finnhub
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=API_KEY)

print(finnhub_client.company_basic_financials("YHC", "all"))