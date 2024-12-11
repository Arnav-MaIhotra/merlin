import pandas as pd
import yfinance as yf
import random

stocks_csv_path = "nasdaq_screener.csv"
industry_csv_path = "industry_pe_averages.csv"

stocks_df = pd.read_csv(stocks_csv_path)
industry_df = pd.read_csv(industry_csv_path)

def get_pe_ratio(symbol):
    try:
        stock = yf.Ticker(symbol)
        pe_ratio = stock.info.get('trailingPE')
        return pe_ratio
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

stocks_df['P/E Ratio'] = stocks_df['Symbol'].apply(get_pe_ratio)

merged_df = pd.merge(stocks_df, industry_df, on="Industry", how="left")
merged_df['Difference'] = merged_df['P/E Ratio'] - merged_df['Average P/E Ratio']

sorted_differences = merged_df.groupby('Industry').apply(
    lambda group: group[['Symbol', 'Difference']].sort_values(by='Difference')
)

sorted_differences = sorted_differences.dropna(axis=0)

sorted_differences.to_csv("pe_ratio_industry_avg_diff.csv")