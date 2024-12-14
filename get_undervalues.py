import pandas as pd
import yfinance as yf
import time
import math

def calculate_rsi(data, period=14):
    delta = data.diff(1)

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1].values[0]

stocks_csv_path = "nasdaq_screener.csv"
industry_csv_path = "industry_pe_averages.csv"

stocks_df = pd.read_csv(stocks_csv_path).sample(250)
industry_df = pd.read_csv(industry_csv_path)

total = len(stocks_df)

pe_diffs = {}

rsi_diffs = {}

for i in stocks_df["Symbol"].values:
    try:
        industry = stocks_df["Industry"][stocks_df.index[stocks_df["Symbol"] == i]].values[0]
        industry_pe = industry_df["P/E Ratio"][industry_df.index[industry_df["Industry"] == industry]].values[0]
        
        stock = yf.Ticker(i)
        pe_ratio = stock.info.get('trailingPE')

        if pe_ratio:
            pe_ratio = float(pe_ratio)
            pe_diffs[i] = (pe_ratio-industry_pe)/industry_pe
        else:
            None
        rsi_data = yf.download(i, period="1mo", interval="1d")

        rsi = calculate_rsi(rsi_data["Adj Close"].tail(14))

        rsi_diffs[i] = (rsi-30)/30
    except Exception as e:
        print(e)

rsi_diffs = {key: value for key, value in rsi_diffs.items() if value != -1 and not (isinstance(value, float) and math.isnan(value))}

pe_diffs = {key: value for key, value in pe_diffs.items() if not (isinstance(value, float) and math.isnan(value))}

common_symbols = rsi_diffs.keys() & pe_diffs.keys()

undervalue_scores = {k: (pe_diffs[k]*0.7 + rsi_diffs[k]*0.3)*-100 for k in common_symbols}

diffs = dict(sorted(undervalue_scores.items(), key=lambda item: item[1], reverse=True))

pd.DataFrame.from_dict({"Ticker":tuple(diffs.keys()), "Undervalue Score":tuple(diffs.values())}).to_csv("undervalue_score.csv", index=False)