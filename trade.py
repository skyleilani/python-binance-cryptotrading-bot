from binance import Client
import pandas as pd
from matplotlib import pyplot as plt

api_secret = "NQn0q2WkevPpBgxGuApVgaHZs1YdXM3u4kTzNAgdgS25QdGfsezrfbXlvRoiw80R"
api_key = "CVep5onAnPW24gJnnfqFCI22FlJoC26WgmCF9TVmj2k33ZSyiKcLUna1x1SQmWxD"

client = Client(api_key, api_secret, tld="us")

# getminutedata:
#    returns a data frame of currency price info on your cryptocurrency
#    from the last 30 minutes, indexed by the minute
# symbol - 
# interval - 
# lookback - 
def getminutedata(symbol, interval, lookback): 
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback+' m ago UTC'))
    # cuts the frame by index from 30rowx12column -> 30rows x 5 columns
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    # sets the index of data frame to 'Time' for so our output is measured by timestamps
    frame = frame.set_index('Time')
    # translate timestamps from unix time to normal time
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float) # translates data from being string to being float 

    return frame

# analyzing cryptos
cryptodata = getminutedata('BTCUSDT', '1m', '30')
plt.plot(cryptodata)
plt.show()

