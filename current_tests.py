import yfinance as yf
import json

data = yf.download("AIMD", start="2019-09-30")
print(data)