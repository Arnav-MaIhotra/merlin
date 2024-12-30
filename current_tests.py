import finnhub
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

basics = finnhub_client.company_basic_financials("AAPL", "all").get("series").get("quarterly")

print(basics.keys())

financials = finnhub_client.financials("AAPL", "bs", "quarterly").get("financials")

for i in financials:
    print(i)

reported = finnhub_client.financials_reported(symbol="AAPL", freq="quarterly").get("data")

for i in reported:
    print(i.keys())