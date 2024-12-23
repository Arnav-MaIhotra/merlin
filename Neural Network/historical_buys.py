import pandas as pd

data = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\10y_data.csv")

ticker = []
growth = []
date = []

for i in data.columns[1:]:
    stock_df = data[["Date", i]]
    if len(stock_df.dropna()) == 0:
        continue
    count = 0
    while count < (len(stock_df)-7):
        diff = (stock_df[i][count+7]-stock_df[i][count])/stock_df[i][count]
        if diff > 0.2:
            ticker.append(i)
            growth.append(diff)
            date.append(stock_df["Date"][count])
            count += 6
        count += 1

buys = pd.DataFrame({"Ticker":ticker, "Growth":growth, "Date":date})

buys.to_csv(r"Neural Network\10y_buys.csv", index=False)