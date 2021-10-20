# Imports crypto currency pair OHLCV data from binance
# Saves as .csv formatted specifically for RealTest


import ccxt
import pandas as pd
import pathlib


# All tickers must be the format ---> 'BASE/QUOTE' <----
# You can add non USDT pairs, such as 'BTC/BNB' etc
# However, that may get confusing.

tickers = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']
timeframe = '1d'    # 1d 1h 5m etc
since = 100         # how many days do you want data for 

# Depending on your operating system and setup, this may take some trial and error.
# With nothing below it outputs in the current directory.
# Include a / at the end if you are naming the folder to use.
filepath = pathlib.Path(__file__).parent.resolve()


    # Fetch OHLCV data 
    #
    #  @staticmethod
def fetchOHLCVData(symbol: str, timeframe: str, days: int = 30) -> list:
        exchange = ccxt.binance({
           'timeout': 10000,
           'enableRateLimit': True,
           'rateLimit': 250,            # don't lower this... you can get IP banned.
           'options': {
               'defaultType': 'future',
            
           }
       })
        exchange.loadMarkets()

        # Get all OHLCV data since
        since = exchange.milliseconds() - days * 24 * 60 * 60 * 1000

        # Data container
        ohlcv_data = []

        # Paginate through data
        while since < exchange.milliseconds():

            #Fetch OHLCV data
            ohlcv =  exchange.fetchOHLCV(symbol, timeframe=timeframe, since=since)

            # Did we received enough valid data
            if ohlcv and len(ohlcv) > 1:
                since = ohlcv[-1][0] + (ohlcv[-1][0] - ohlcv[-2][0])

                # Append OHLCV data
                ohlcv_data += ohlcv
            else:
                break

        # Return OHLCV data
        return ohlcv_data

def data_to_df(data):
    df = pd.DataFrame(data, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Timestamp'] = pd.to_datetime(df.Timestamp, unit='ms')
    df = df.set_index('Timestamp')
    return df

counter = 0
for coin in tickers:
    data = fetchOHLCVData(coin, timeframe, since)
    df = data_to_df(data)
    coin = coin.replace("/","")
    df.to_csv(f'{filepath}/{coin}.CSV')
    counter +=1
    print(f'{coin} updated.')
    # print(df.tail(2))

print(f'{len(tickers)} tickers chosen, {counter} updated.')