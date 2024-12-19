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

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    balance_sheet = stock.balance_sheet
    working_capital = (
        balance_sheet.loc['Current Assets'].iloc[0] - balance_sheet.loc['Current Liabilities'].iloc[0]
    )
    total_assets = balance_sheet.loc['Total Assets'].iloc[0]
    total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
    
    income_statement = stock.financials
    try:
        ebit = income_statement.loc['EBIT'].iloc[0]
    except KeyError:
        try:
            ebit = income_statement.loc['Operating Income'].iloc[0]
        except KeyError:
            ebit = income_statement.loc['EBITDA'].iloc[0]
    
    sales = income_statement.loc['Total Revenue'].iloc[0]
    
    retained_earnings = balance_sheet.loc['Retained Earnings'].iloc[0]

    market_cap = stock.info['marketCap']

    return {
        "working_capital": working_capital,
        "total_assets": total_assets,
        "retained_earnings": retained_earnings,
        "ebit": ebit,
        "market_value_equity": market_cap,
        "total_liabilities": total_liabilities,
        "sales": sales,
    }

def calculate_altman_z_score(data):
    z_score = (
        1.2 * (data['working_capital'] / data['total_assets']) +
        1.4 * (data['retained_earnings'] / data['total_assets']) +
        3.3 * (data['ebit'] / data['total_assets']) +
        0.6 * (data['market_value_equity'] / data['total_liabilities']) +
        1.0 * (data['sales'] / data['total_assets'])
    )
    return z_score

stocks_csv_path = "nasdaq_screener.csv"
industry_csv_path = "industry_pe_averages.csv"

stocks_df = pd.read_csv(stocks_csv_path).sample(200)
industry_df = pd.read_csv(industry_csv_path)

total = len(stocks_df)

pe_diffs = {}

rsi_diffs = {}

pb_diffs = {}

altman_z_diffs = {}

count = 0

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

        pb_ratio = stock.info.get('priceToBook')

        if pb_ratio:
            pb_ratio = float(pb_ratio)
            pb_diffs[i] = (pb_ratio-1)

        z_score_data = get_financial_data(i)
        altman_z = calculate_altman_z_score(z_score_data)

        altman_z_diffs[i] = (1.81-altman_z)/1.81
    except Exception as e:
        print(e)
    
    count += 1

rsi_diffs = {key: value for key, value in rsi_diffs.items() if value != -1 and not (isinstance(value, float) and math.isnan(value))}

pe_diffs = {key: value for key, value in pe_diffs.items() if not (isinstance(value, float) and math.isnan(value))}

common_symbols = rsi_diffs.keys() & pe_diffs.keys() & pb_diffs.keys() & altman_z_diffs.keys()

undervalue_scores = {k: (pe_diffs[k]*0.35 + pb_diffs[k]*0.35 + rsi_diffs[k]*0.1 + altman_z_diffs[k]*0.2)*-100 for k in common_symbols}

diffs = dict(sorted(undervalue_scores.items(), key=lambda item: item[1], reverse=True))

pd.DataFrame.from_dict({"Ticker":tuple(diffs.keys()), "Undervalue Score":tuple(diffs.values())}).to_csv("undervalue_score_3.csv", index=False)