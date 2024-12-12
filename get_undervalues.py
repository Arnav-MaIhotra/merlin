import pandas as pd
import yfinance as yf
import time

stocks_csv_path = "nasdaq_screener.csv"
industry_csv_path = "industry_pe_averages.csv"

stocks_df = pd.read_csv(stocks_csv_path)
industry_df = pd.read_csv(industry_csv_path)

for i in stocks_df["Symbol"].values:
        print(i)
        industry = stocks_df["Industry"][stocks_df.index[stocks_df["Symbol"] == i]].values[0]
        industry_pe = industry_df["P/E Ratio"][industry_df.index[industry_df["Industry"] == industry]].values[0]
        
        stock = yf.Ticker(i)
        pe_ratio = stock.info.get('trailingPE')

        if pe_ratio:
            pe_ratio = float(pe_ratio)
        else:
            continue