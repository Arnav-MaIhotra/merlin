import pandas as pd

data = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\10y_data.csv")

ticker_buys = []
growth_buys = []
date_buys = []

ticker_sells = []
growth_sells = []
date_sells = []

for i in data.columns[1:]:
    stock_df = data[["Date", i]]
    if len(stock_df.dropna()) == 0:
        continue
    count = 0
    while count < (len(stock_df)-7):
        diff = (stock_df[i][count+7]-stock_df[i][count])/stock_df[i][count]
        if diff > 0.2:
            ticker_buys.append(i)
            growth_buys.append(diff)
            date_buys.append(stock_df["Date"][count])
            count += 6
        if diff < -0.2:
            ticker_sells.append(i)
            growth_sells.append(diff)
            date_sells.append(stock_df["Date"][count])
            count += 6
        count += 1

buys = pd.DataFrame({"Ticker":ticker_buys, "Growth":growth_buys, "Date":date_buys})

buys.to_csv(r"Neural Network\10y_buys.csv", index=False)

sells = pd.DataFrame({"Ticker":ticker_sells, "Growth":growth_sells, "Date":date_sells})

sells.to_csv(r"Neural Network\10y_sells.csv", index=False)