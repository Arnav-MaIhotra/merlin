import finnhub
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

ticker = "AAPL"

bs = finnhub_client.financials(ticker, "bs", "quarterly").get("financials")

ic = finnhub_client.financials(ticker, "ic", "quarterly").get("financials")

shares_outstandings = {}

for i in bs:
    date = i.get("period")
    shares_outstandings[date] = i.get("sharesOutstanding")
ebits = {}

revenues = {}

for i in ic:
    date = i.get("period")
    revenues[date] = i.get("revenue")
    ebits[date] = i.get("ebit")

ticker_z_scores = {}

for i in bs:
    working_capital = i.get("currentAssets") - i.get("currentLiabilities")
    total_assets = i.get("totalAssets")

    term_1 = 1.2*working_capital/total_assets

    retained_earnings = i.get("retainedEarnings")

    term_2 = 1.4*retained_earnings/total_assets

    date = i.get("period")

    ebit = ebits[date]

    term_3 = 3.3*ebit/total_assets

    price = yf.download(ticker, start=date)["Close"].values[0][0]

    shares_outstanding = shares_outstandings[date]

    mktcap = shares_outstanding*price

    total_liabilities = i.get("totalLiabilities")

    term_4 = 0.6*mktcap/total_liabilities

    sales = revenues[date]

    term_5 = sales/total_assets

    z_score = term_1+term_2+term_3+term_4+term_5

    ticker_z_scores[date] = z_score

print(ticker_z_scores)