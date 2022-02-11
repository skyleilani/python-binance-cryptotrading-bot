from binance import Client
import pandas as pd

api_secret = "NQn0q2WkevPpBgxGuApVgaHZs1YdXM3u4kTzNAgdgS25QdGfsezrfbXlvRoiw80R"

api_key = "CVep5onAnPW24gJnnfqFCI22FlJoC26WgmCF9TVmj2k33ZSyiKcLUna1x1SQmWxD"

client = Client(api_key, api_secret, tld="us")

# print(pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 m ago UTC')))

def getminutedata(symbol, interval, lookback): 
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' m ago UTC'))
    print(frame)

    return frame

getminutedata('BTCUSDT', '1m', '30')


# def getminutedata(symbol, interval, lookback):
#     frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' min ago UTC'))
#     print(frame)
#     frame = frame.iloc[:,:6]

#     frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
#   #set index of data frame to time - timestamps as index (its given in unix time (seconds since the year 1970 lol))
#   # all numbers are stored as strings in the data frame, youll have to later transform these to float values
#     frame = frame.set_index('Time')

# #so we're going to translate the unix time to normal timestap 

#     frame.index = pd.to_datetime(frame.index, unit='ms')
#     frame = frame.astype(float)
#     return frame


# getminutedata('BTCUSDT','1m', '30')