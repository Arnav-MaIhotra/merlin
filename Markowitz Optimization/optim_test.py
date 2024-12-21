import yfinance as yf

with open("stock_allocations_1m_3y.csv", "r") as file:
    sum_ = 0
    for i in file:
        j = i.replace("[", "").replace("]", "").split(", ")
        price = yf.Ticker(j[0][1:-1]).fast_info.get("lastPrice")
        sum_ += price*float(j[1])
    print((sum_-1000000)/1000000/3, sum_)