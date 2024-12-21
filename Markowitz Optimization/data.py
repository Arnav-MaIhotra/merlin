import yfinance
import pandas as pd
import datetime
import numpy as np

data = yfinance.download("NVDA", period="6mo")

dates = data.index

i_ = 0

for i in dates:
    