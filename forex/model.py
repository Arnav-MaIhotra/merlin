import yfinance as yf

currencies = usd_currency_pairs = [
 "EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY", "USD/CHF", "USD/CAD", "NZD/USD", "USD/SGD", "USD/HKD", "USD/MXN", "USD/TRY", "USD/INR", "USD/ZAR", "USD/KRW", "USD/BRL", "USD/RUB", "USD/THB", "USD/IDR", "USD/CLP", "USD/PKR", "USD/EGP", "USD/NGN", "USD/BDT", "USD/VND", "USD/AED", "USD/KWD"]

for currency in currencies:

    currency = currency.replace("/", "")+"=X"

    forex_data = yf.download(currency, end="2025-1-1")

    forex_data.to_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\forex\forex_data\{}.csv".format(currency.replace("/", "").replace("=X", "")))