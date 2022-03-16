from binance import Client
import pandas as pd
from matplotlib import pyplot as plt

api_secret = "apisec"
api_key = "apikey"

client = Client(api_key, api_secret, tld="us")
print("successful sign in")

# getdatabymin:
#    returns a data frame of currency price info on your cryptocurrency
#    from the last 30 minutes, indexed by the minute
# symbol - 
# interval - 
# lookback - 
def getdatabymin(symbol, interval, lookback): 
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
cryptodata = getdatabymin('DOGEUSDT', '1m', '30')
plt.plot(cryptodata)
plt.show()

# SAMPLE TRADING STRATEGY!!!!! NOT 0
# triggers purchase if asset sees a decrease of more than 0.2% 
# within the last 30 minutes. 
# sells if asset increases by more than 
# 0.15% <- must be your profit in a trade
# or (for risk) sell if it decreases more than 0.15%

def tradingstrat(symbol, qty, orderplaced=False): 
    # create data frame
    df = getminutedata(symbol, '1m', '30')

    # cumulative return - 
    # total change in the investment price over a certain  period of time. 
    # this helps you to keep track of the gain or loss of an investment.
    # how has your asset been performing over the last 30 minutes?

    # cumulative return from over the last 30 minutes
    cumulativereturn = (df.Open.pct_change() + 1).cumprod() - 1
    if not orderplaced: 
        # set buying condition for if asset hasn't been purchased yet
        if cumulativereturn[-1] < -0.002: 

            #check documentation & study for new args here 
            order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quantity=qty)
            
            print(order)
            orderplaced = True

        else: 
            print('no trade executed ')
    
    if orderplaced:
        # every minute you're sending requests to see how the asset is performing
        # this is an endless loop..... :( 
    
        while True: 
            df = getminutedata(symbol, '1m', '30m')
            # sincebuy data frame contains only timestamps AFTER we have bought asset
            sincebuy= df.loc[df.index > pd.to_datetime(
            order['transactTime'], unit='ms')]

            # the first few bits of data right after asset has been bought
            # in sincebuy could be empty because theres just not new data in the very first minute or so 
            if len(sincebuy) > 0: 
                sincebuyret = (df.Open.pct_change() + 1).cumprod() - 1
