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

shifts = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v1\sell_metrics_v1.csv")

count = 0

limit_count = 0

tickers = []
growths = []
dates = []
pe_ratios = []
pb_ratios = []

pb_ratio_data = {}

for i in shifts.T:
    try:
        line = dict(shifts.iloc[i])
        ticker = line["Ticker"]
        growth = line["Growth"]
        date = line["Date"]
        pe_ratio = line["P/E Ratio"]

        pb_data = None

        if ticker in pb_ratio_data.keys():
            pb_data = pb_ratio_data[ticker]
        else:
            target_date = datetime.strptime(date, '%Y-%m-%d')
            closest_record = None

            financials = finnhub_client.company_basic_financials(ticker, 'all')

            pb_data = financials.get('series').get('quarterly').get('pb')

            pb_ratio_data[ticker] = pb_data

            limit_count += 1

        for record in pb_data:
            record_date = datetime.strptime(record['period'], '%Y-%m-%d')
            if record_date <= target_date:
                if closest_record is None or record_date > datetime.strptime(closest_record['period'], '%Y-%m-%d'):
                    closest_record = record
        
        pb_old = closest_record['v'] if closest_record else None

        if pb_old:
            prices = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\stock_data\\{}.csv".format(ticker)).iloc[2:].reset_index(drop=True).rename({"Price":"Date"}, axis=1)

            price = prices.iloc[prices[prices["Date"] == date].index.values[0]]["Close"]

            try:

                old_price_data = yf.download(ticker, closest_record['period'], date)["Close"]
                if old_price_data.empty:
                    time.sleep(45)
                    old_price_data = yf.download(ticker, closest_record['period'], date)["Close"]

                old_price = old_price_data.iloc[0].values[0]

                pb_ratio = float(price)*pb_old/float(old_price)
            
            except:
                pb_ratio = pb_old

            pb_ratios.append(pb_ratio)
            tickers.append(ticker)
            growths.append(growth)
            dates.append(date)
            pe_ratios.append(pe_ratio)
    except:
        None
        

    count += 1
    #if limit_count % 300 == 0:
        #sys.stdout = sys.__stdout__
        #sys.stderr = sys.__stderr__

        #print(count*100/len(shifts))
        #time.sleep(61)

        #sys.stdout = open(os.devnull, 'w')
        #sys.stderr = open(os.devnull, 'w')

    if count % 1000 == 0:
        print(count*100/len(shifts))
        #time.sleep(120)
    #if count % 10000 == 0:
        #time.sleep(300)


df = pd.DataFrame({"Ticker":tickers, "Growth":growths, "Date":dates, "P/E Ratio":pe_ratios, "P/B Ratio":pb_ratios})

df.to_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v2\sell_metrics_v2.csv", index=False)