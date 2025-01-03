from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime
import time
import ccxt
import cryptocompare

cg = CoinGeckoAPI()

def get_historical_data(crypto_id='bitcoin', currency='usd', days=30):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    historical_data = cg.get_coin_market_chart_range_by_id(id=crypto_id, vs_currency=currency, from_timestamp=start_timestamp, to_timestamp=end_timestamp)
    
    prices = historical_data['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

df = get_historical_data()
print(df)

exchange = ccxt.kraken()

def get_binance_historical_data(symbol='BTC/USDT', timeframe='1d', since=None):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

since = exchange.parse8601('2023-12-02T00:00:00Z')
df = get_binance_historical_data(symbol='BTC/USDT', timeframe='1d', since=since)
print(df)

exchange = ccxt.coinbase()

def get_coinbasepro_historical_data(symbol='BTC/USD', timeframe='1d', since=None):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

since = exchange.parse8601('2023-12-02T00:00:00Z')
df = get_coinbasepro_historical_data(symbol='BTC/USD', timeframe='1d', since=since)
print(df)

def get_historical_price(crypto='BTC', currency='USD', limit=30):
    historical_data = cryptocompare.get_historical_price_day(crypto, currency, limit=limit)
    df = pd.DataFrame(historical_data)
    return df

df = get_historical_price(crypto='BTC', currency='USD', limit=30)
print(df)