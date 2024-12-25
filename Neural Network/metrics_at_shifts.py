import finnhub
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime, timedelta
import time
import sys

#sys.stdout = open(os.devnull, 'w')
#sys.stderr = open(os.devnull, 'w')

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(API_KEY)

shifts = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\10y_buys.csv")

count = 0

tickers = []
growths = []
dates = []
pe_ratios = []

for i in shifts.T:
    line = dict(shifts.iloc[i])
    ticker = line["Ticker"]
    growth = line["Growth"]
    date = line["Date"]

    financials = finnhub_client.company_basic_financials(ticker, 'all')

    eps_data = financials.get('series', {}).get('quarterly', {}).get('eps', [])

    target_date = datetime.strptime(date, '%Y-%m-%d')
    closest_record = None

    for record in eps_data:
        record_date = datetime.strptime(record['period'], '%Y-%m-%d')
        if record_date <= target_date:
            if closest_record is None or record_date > datetime.strptime(closest_record['period'], '%Y-%m-%d'):
                closest_record = record

    eps = closest_record['v'] if closest_record else None

    if eps:

        price = yf.download(ticker, start=date, end=(datetime.strptime(date, "%Y-%m-%d")+timedelta(days=7)).strftime("%Y-%m-%d"))["Close"].iloc[0].values[0]

        pe_ratio = price/eps

        tickers.append(ticker)
        growths.append(growth)
        dates.append(date)
        pe_ratios.append(pe_ratio)
    
    else:
        None

    count += 1
    if count % 300 == 0:
        #sys.stdout = sys.__stdout__
        #sys.stderr = sys.__stderr__

        print(count*100/len(shifts))
        time.sleep(61)

        #sys.stdout = open(os.devnull, 'w')
        #sys.stderr = open(os.devnull, 'w')


df = pd.DataFrame({"Ticker":tickers, "Growth":growths, "Date":dates, "P/E Ratios":pe_ratios})

df.to_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\buy_metrics_v1.csv", index=False)

time.sleep(61)

shifts = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\10y_sells.csv")

count = 0

tickers = []
growths = []
dates = []
pe_ratios = []

for i in shifts.T:
    line = dict(shifts.iloc[i])
    ticker = line["Ticker"]
    growth = line["Growth"]
    date = line["Date"]

    financials = finnhub_client.company_basic_financials(ticker, 'all')

    eps_data = financials.get('series', {}).get('quarterly', {}).get('eps', [])

    target_date = datetime.strptime(date, '%Y-%m-%d')
    closest_record = None

    for record in eps_data:
        record_date = datetime.strptime(record['period'], '%Y-%m-%d')
        if record_date <= target_date:
            if closest_record is None or record_date > datetime.strptime(closest_record['period'], '%Y-%m-%d'):
                closest_record = record

    eps = closest_record['v'] if closest_record else None

    if eps:

        price = yf.download(ticker, start=date, end=(datetime.strptime(date, "%Y-%m-%d")+timedelta(days=7)).strftime("%Y-%m-%d"))["Close"].iloc[0].values[0]

        pe_ratio = price/eps

        tickers.append(ticker)
        growths.append(growth)
        dates.append(date)
        pe_ratios.append(pe_ratio)
    
    else:
        None

    count += 1
    if count % 300 == 0:
        #sys.stdout = sys.__stdout__
        #sys.stderr = sys.__stderr__

        print(count*100/len(shifts))
        time.sleep(61)

        #sys.stdout = open(os.devnull, 'w')
        #sys.stderr = open(os.devnull, 'w')


df = pd.DataFrame({"Ticker":tickers, "Growth":growths, "Date":dates, "P/E Ratios":pe_ratios})

df.to_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\sell_metrics_v1.csv", index=False)