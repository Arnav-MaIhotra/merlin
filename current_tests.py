import finnhub
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

bs = finnhub_client.financials("AAPL", "bs", "quarterly").get("financials")

ic = finnhub_client.financials("AAPL", "ic", "quarterly").get("financials")

cf = finnhub_client.financials("AAPL", "cf", "quarterly").get("financials")

for i in ic:
    print(i)

for i in bs:
    print(i)

reported = finnhub_client.financials_reported(symbol="AAPL", freq="quarterly").get("data")

ebits = {}

for i in ic:
    date = i.get("period")
    ebits[date] = i.get("ebit")

for i in bs:
    working_capital = i.get("currentAssets") - i.get("currentLiabilities")
    total_assets = i.get("totalAssets")

    term_1 = 1.2*working_capital/total_assets

    retained_earnings = i.get("retainedEarnings")

    term_2 = 1.4*retained_earnings/total_assets

    date = i.get("period")

    ebit = ebits[date]

    term_3 = 3.3*ebit/total_assets