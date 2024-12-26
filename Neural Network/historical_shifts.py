import pandas as pd
import os

files = os.listdir(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\stock_data")

ticker_buys = []
growth_buys = []
date_buys = []

ticker_sells = []
growth_sells = []
date_sells = []

for i in files:
    stock_df = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\stock_data\{}".format(i)).iloc[2:].reset_index(drop=True).rename({"Price":"Date"}, axis=1)
    dates = stock_df["Date"]
    closes = stock_df["Close"]
    if len(stock_df.dropna()) == 0:
        continue
    count = 0
    while count < (len(stock_df)-1):
        diff = (float(closes.iloc[count+1])-float(closes.iloc[count]))/float(closes.iloc[count])
        if diff > 0.2:
            ticker_buys.append(i[0:-4])
            growth_buys.append(diff)
            date_buys.append(dates.iloc[count])
        if diff < -0.2:
            ticker_sells.append(i[0:-4])
            growth_sells.append(diff)
            date_sells.append(dates.iloc[count])
        count += 1

buys = pd.DataFrame({"Ticker":ticker_buys, "Growth":growth_buys, "Date":date_buys})

buys.to_csv(r"Neural Network\historical_buys.csv", index=False)

sells = pd.DataFrame({"Ticker":ticker_sells, "Growth":growth_sells, "Date":date_sells})

sells.to_csv(r"Neural Network\historical_sells.csv", index=False)