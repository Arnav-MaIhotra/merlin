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

shifts = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v2\sell_metrics_v2.csv")

count = 0

limit_count = 0

tickers = []
growths = []
dates = []
pe_ratios = []
pb_ratios = []
z_scores = []

altman_z_score_data = {}

for i in shifts.T:
    try:
        line = dict(shifts.iloc[i])
        ticker = line["Ticker"]
        growth = line["Growth"]
        date = line["Date"]
        pe_ratio = line["P/E Ratio"]
        pb_ratio = line["P/B Ratio"]

        z_score_data = None

        if ticker in altman_z_score_data.keys():
            z_score_data = altman_z_score_data[ticker]
        else:
            closest_record = None

            target_date = datetime.strptime(date, '%Y-%m-%d')

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

            z_score_data = {}

            for i in bs:
                try:
                    working_capital = i.get("currentAssets") - i.get("currentLiabilities")
                    total_assets = i.get("totalAssets")

                    term_1 = 1.2*working_capital/total_assets

                    retained_earnings = i.get("retainedEarnings")

                    term_2 = 1.4*retained_earnings/total_assets

                    date = i.get("period")

                    ebit = ebits[date]

                    term_3 = 3.3*ebit/total_assets

                    price_data = yf.download(ticker, start=date)["Close"]
                    while price_data.empty:
                        print(count*100/len(shifts))
                        time.sleep(30)
                        price_data = yf.download(ticker, start=date)["Close"]
                    price = price_data.values[0][0]

                    shares_outstanding = shares_outstandings[date]

                    mktcap = shares_outstanding*price

                    total_liabilities = i.get("totalLiabilities")

                    term_4 = 0.6*mktcap/total_liabilities

                    sales = revenues[date]

                    term_5 = sales/total_assets

                    z_score = term_1+term_2+term_3+term_4+term_5

                    z_score_data[date] = z_score
                except:
                    None
            
            altman_z_score_data[ticker] = z_score_data

            limit_count += 2

        for record in z_score_data:
            record_date = datetime.strptime(record, '%Y-%m-%d')
            if record_date <= target_date:
                if closest_record is None or record_date > datetime.strptime(closest_record, '%Y-%m-%d'):
                    closest_record = record
        
        z_score = z_score_data[closest_record] if closest_record else None

        if z_score:
            tickers.append(ticker)
            growths.append(growth)
            dates.append(date)
            pe_ratios.append(pe_ratio)
            pb_ratios.append(pb_ratio)
            z_scores.append(z_score)
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

    #if count % 1000 == 0:
        #print(count*100/len(shifts))
        #time.sleep(120)
    #if count % 10000 == 0:
        #time.sleep(300)


df = pd.DataFrame({"Ticker":tickers, "Growth":growths, "Date":dates, "P/E Ratio":pe_ratios, "P/B Ratio":pb_ratios, "Altman Z-Score":z_scores})

df.to_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v3\sell_metrics_v3.csv", index=False)