import vectorbt as vbt

price = vbt.YFData.download("NVDA", start="1999-01-22", end="2024-11-20").get("Close")

price.to_csv("temp_data.csv")