import pandas as pd
import yfinance_cache as yf
import time

stocks_csv_path = "nasdaq_screener.csv"
industry_csv_path = "industry_pe_averages.csv"

stocks_df = pd.read_csv(stocks_csv_path).sample(200)
industry_df = pd.read_csv(industry_csv_path)

total = len(stocks_df)

diffs = {}

count = 0

for i in stocks_df["Symbol"].values:
    try:
        industry = stocks_df["Industry"][stocks_df.index[stocks_df["Symbol"] == i]].values[0]
        industry_pe = industry_df["P/E Ratio"][industry_df.index[industry_df["Industry"] == industry]].values[0]
        
        stock = yf.Ticker(i)
        pe_ratio = stock.info.get('trailingPE')

        if pe_ratio:
            pe_ratio = float(pe_ratio)
            diffs[i] = (pe_ratio-industry_pe)/industry_pe
        else:
            continue
    except:
            None
    count += 1
    if count % 250 == 0:
        print(round(count*100/total, 2))
        time.sleep(20)
    if count % 500 == 0:
         time.sleep(120)

try:

    diffs = dict(sorted(diffs.items(), key=lambda item: item[1]))

    pd.DataFrame.from_dict({"Ticker":tuple(diffs.keys()), "P/E Ratio % Change":tuple(diffs.values())}).to_csv("pe_ratio_industry_avg_diff.csv", index=False)

except:
     
    ln = input(">>> ")
    exec(ln)