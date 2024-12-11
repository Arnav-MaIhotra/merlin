import pandas as pd
import yfinance as yf
import time

csv_file = "nasdaq_screener.csv"
data = pd.read_csv(csv_file)

pe_ratios = {}

count = 0

for index, row in data.iterrows():
    count += 1

    symbol = row['Symbol']
    industry = row['Industry']
    
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        pe_ratio = info.get('trailingPE')
        
        if pe_ratio and industry:
            if industry not in pe_ratios:
                pe_ratios[industry] = []
            pe_ratios[industry].append(float(pe_ratio))
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

    if count % 250 == 0:
        print(symbol)
        time.sleep(120)

industry_averages = {industry: sum(ratios) / len(ratios) for industry, ratios in pe_ratios.items()}

industry_avg_df = pd.DataFrame(list(industry_averages.items()), columns=['Industry', 'Average P/E Ratio'])

industry_avg_df.to_csv("industry_pe_averages.csv", index=False)
print(industry_avg_df)