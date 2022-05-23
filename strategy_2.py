#Importing libraries
import pandas as pd
from requests.sessions import session
import yfinance as yf
import numpy as np
import datetime as dt
from datetime import date
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.momentum import StochRSIIndicator, rsi, stoch
from ta.trend import MACD, macd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator





#Importing tickers
df = pd.read_excel('backtest1-test1.xlsx')
tickers = df['Tickers'].values.tolist()
# tickers = ['AAPL', 'FB', 'GOOG', 'F']
tickers = sorted(tickers)


#Creating global dataframe.
df = yf.download(tickers, start='2009-10-01')
df.index = df.index.date


#Creating Adjusted Close dataframe.
adj_close_df = df['Adj Close']
open_df = df['Open']
close_df = df['Close']
low_df = df['Low']




#START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL
#START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL
#START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL - START BUY SIGNAL

#START ENGULFING (based on SNIPER-62)
#START ENGULFING (based on SNIPER-62)
#START ENGULFING (based on SNIPER-62)
df_eng = df.reset_index()
dates_list = df_eng['index']
del df_eng['index']


df_low = df_eng['Low']
df_open = df_eng['Open']
df_high = df_eng['High']
df_adjclose = df_eng['Adj Close']


#Add first row NaN Low
df1 = pd.DataFrame([[np.nan] * len(df_low.columns)], columns=df_low.columns)
df_low = df1.append(df_low, ignore_index=True)

#Add last row NaN Open
df_open = df_open.append(df1, ignore_index=True)

#Add first row NaN High
df_high = df1.append(df_high, ignore_index=True)

#Add last row NaN AdjClose
df_adjclose = df_adjclose.append(df1, ignore_index=True)


list1 = []
sub_low_open = pd.DataFrame(list1)

for i in df_low:
    sub_low_open[i] = df_low[i] - df_open[i]


list2 = []
sub_adjclose_high = pd.DataFrame(list2)

for i in df_low:
    sub_adjclose_high[i] = df_adjclose[i] - df_high[i]


sub_low_open = sub_low_open.iloc[1:-1]
sub_adjclose_high = sub_adjclose_high.iloc[1:-1]
dates_list = dates_list[1:]


sub_low_open = sub_low_open.mask(sub_low_open>0, 1)
sub_low_open = sub_low_open.mask(sub_low_open<0, 0)


sub_adjclose_high = sub_adjclose_high.mask(sub_adjclose_high>0, 1)
sub_adjclose_high = sub_adjclose_high.mask(sub_adjclose_high<0, 0)


list3 = []
engulfing_signal = pd.DataFrame(list3)

for i in sub_low_open:
    engulfing_signal[i] = sub_low_open[i] + sub_adjclose_high[i]


engulfing_signal = engulfing_signal.mask(engulfing_signal>1.5, 100)
engulfing_signal = engulfing_signal.mask(engulfing_signal<1.49, 0)


engulfing_signal['Date'] = dates_list
engulfing_signal = engulfing_signal.set_index('Date')
# engulfing_signal.index = engulfing_signal.index.date
#END ENGULFING (based on SNIPER-62)
#END ENGULFING (based on SNIPER-62)
#END ENGULFING (based on SNIPER-62)



#START ENGULFING LOWER EMA15 & CO
#START ENGULFING LOWER EMA15 & CO
#START ENGULFING LOWER EMA15 & CO
adj_close_df = df['Adj Close']
high_df = df['High']
open_df = df['Open']
low_df = df['Low']


#Creating the EMA15 dataframe.
list5 = []
ema15_df = pd.DataFrame(list5)

# for i in adj_close_df:
#     ema15_df[i] = talib.EMA(adj_close_df[i], timeperiod=15)

def EMA(data, period=20, column=tickers):
    return data[column].ewm(span=period, adjust=False).mean()

for i in adj_close_df:
    ema15_df[i] = EMA(adj_close_df, period=15, column=i)

#Creating the dataframe witht the difference of EMA15 and high.
df_diff_ema15_high = ema15_df - high_df

df_diff_ema15_high = df_diff_ema15_high.mask(df_diff_ema15_high>0, 1)
df_diff_ema15_high = df_diff_ema15_high.mask(df_diff_ema15_high<0, 0)


# engulf_sig_df = engulfing_signal * df_diff_ema15_high
engulf_sig_df = engulfing_signal
#END ENGULFING LOWER EMA15 & CO
#END ENGULFING LOWER EMA15 & CO
#END ENGULFING LOWER EMA15 & CO



#START AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50
#START AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50
#START AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50

#Creating the RSI(14) DataFrame
list4 = []
rsi_df = pd.DataFrame(list4)

for i in adj_close_df:
    indicator_rsi_df = RSIIndicator(close=close_df[i], window=14)
    rsi_df[i] = indicator_rsi_df.rsi()


#Creating the SMA(4) on the RSI(14)
list5 = []
sma_of_rsi_df = pd.DataFrame(list5)

for i in rsi_df:
    indicator_sma_rsi_df = SMAIndicator(close=rsi_df[i], window=8)
    sma_of_rsi_df[i] = indicator_sma_rsi_df.sma_indicator()

sma_of_rsi_df = sma_of_rsi_df.mask(sma_of_rsi_df<40, 0)
sma_of_rsi_df = sma_of_rsi_df.mask(sma_of_rsi_df>50, 0)
sma_of_rsi_df = sma_of_rsi_df.mask(sma_of_rsi_df>35, 1)

#END AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50
#END AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50
#END AVERAGE OF LAST 4 RSI(14) BETWEEN 40-50



#START ENGULFING OPEN BELOW 1.5 STD(SMA14)
#START ENGULFING OPEN BELOW 1.5 STD(SMA14)
#START ENGULFING OPEN BELOW 1.5 STD(SMA14)
list6 = []
bb_low_df = pd.DataFrame(list6)

for i in adj_close_df:
    indicator_bb = BollingerBands(close=adj_close_df[i], window=14, window_dev=1.5)
    bb_low_df[i] = indicator_bb.bollinger_lband()


diff_open_15std_df = bb_low_df - open_df

diff_open_15std_df = diff_open_15std_df.mask(diff_open_15std_df>0, 1)
diff_open_15std_df = diff_open_15std_df.mask(diff_open_15std_df<0, 0)
#END ENGULFING OPEN BELOW 1.5 STD(SMA14)
#END ENGULFING OPEN BELOW 1.5 STD(SMA14)
#END ENGULFING OPEN BELOW 1.5 STD(SMA14)



#START AVERAGE STOCHRSI BELOW 25
#START AVERAGE STOCHRSI BELOW 25
#START AVERAGE STOCHRSI BELOW 25
list7 = []
stoch_rsi_d_df = pd.DataFrame(list7)

for i in adj_close_df:
    indicator_stochrsi = StochRSIIndicator(close=adj_close_df[i], window=14, smooth1=3, smooth2=3, fillna=False)
    stoch_rsi_d_df[i] = indicator_stochrsi.stochrsi_d()


list8 = []
stoch_rsi_k_df = pd.DataFrame(list8)

for i in adj_close_df:
    indicator_stochrsi = StochRSIIndicator(close=adj_close_df[i], window=14, smooth1=3, smooth2=3, fillna=False)
    stoch_rsi_k_df[i] = indicator_stochrsi.stochrsi_k()


stoch_rsi_d_df = stoch_rsi_d_df*100
stoch_rsi_k_df = stoch_rsi_k_df*100

stoch_rsi_avg = (stoch_rsi_d_df + stoch_rsi_k_df)/2

stoch_rsi_avg = stoch_rsi_avg.mask(stoch_rsi_avg<25, 200)
stoch_rsi_avg = stoch_rsi_avg.mask(stoch_rsi_avg<105, 0)
stoch_rsi_avg = stoch_rsi_avg.mask(stoch_rsi_avg>150, 1)
#END AVERAGE STOCHRSI BELOW 25
#END AVERAGE STOCHRSI BELOW 25
#END AVERAGE STOCHRSI BELOW 25



#START BOTH MACD ABOVE 0
#START BOTH MACD ABOVE 0
#START BOTH MACD ABOVE 0
list9 = []
macd_line_df = pd.DataFrame(list9)

for i in adj_close_df:
    indicator_macd_line = MACD(close=adj_close_df[i], window_slow=26, window_fast=12, window_sign=9, fillna=False)
    macd_line_df[i] = indicator_macd_line.macd()


list10 = []
macd_signal_line_df = pd.DataFrame(list10)

for i in adj_close_df:
    indicator_macd_signal_line = MACD(close=adj_close_df[i], window_slow=26, window_fast=12, window_sign=9, fillna=False)
    macd_signal_line_df[i] = indicator_macd_signal_line.macd_signal()


macd_line_df = macd_line_df.mask(macd_line_df>0, 1)
macd_line_df = macd_line_df.mask(macd_line_df<0, 0)

macd_signal_line_df = macd_signal_line_df.mask(macd_signal_line_df>0, 1)
macd_signal_line_df = macd_signal_line_df.mask(macd_signal_line_df<0, 0)


macd_avg = macd_line_df * macd_signal_line_df
#END BOTH MACD ABOVE 0
#END BOTH MACD ABOVE 0
#END BOTH MACD ABOVE 0

buy_sig_df = engulf_sig_df * sma_of_rsi_df * diff_open_15std_df * stoch_rsi_avg * macd_avg

#END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL
#END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL
#END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL - END BUY SIGNAL





#START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL
#START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL
#START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL - START SELL SIGNAL

#START CLOSE ABOVE 2.5 STD(SMA20)
#START CLOSE ABOVE 2.5 STD(SMA20)
#START CLOSE ABOVE 2.5 STD(SMA20)
list11 = []
bb_high_df = pd.DataFrame(list11)

for i in adj_close_df:
    indicator_bb = BollingerBands(close=adj_close_df[i], window=20, window_dev=2)
    bb_high_df[i] = indicator_bb.bollinger_hband()


diff_close_25std_df = adj_close_df - bb_high_df

diff_close_25std_df = diff_close_25std_df.mask(diff_close_25std_df>0, 101)
diff_close_25std_df = diff_close_25std_df.mask(diff_close_25std_df<0, 0)
#END CLOSE ABOVE 2.5 STD(SMA20)
#END CLOSE ABOVE 2.5 STD(SMA20)
#END CLOSE ABOVE 2.5 STD(SMA20)



#START RSI(14) ABOVE 65
#START RSI(14) ABOVE 65
#START RSI(14) ABOVE 65
def RSI(data, column='Close', new_df_rsi=tickers):
    data['delta_'+column] = data[column].diff()
    data['up_'+column] = data['delta_'+column].clip(lower=0)
    data['down_'+column] = -1*data['delta_'+column].clip(upper=0)
    
    ema_up = data['up_'+column].ewm(com=13, adjust=False).mean()
    ema_down = data['down_'+column].ewm(com=13, adjust=False).mean()
    
    rs = ema_up/ema_down
    new_df_rsi[column] = 100 - (100/(1+rs))



list12 = []
rsi_df = pd.DataFrame(list12)

for i in close_df:
    RSI(close_df, column=i, new_df_rsi=rsi_df)

copy_rsi_df = rsi_df

rsi_df = rsi_df.mask(rsi_df>=65, 102)
rsi_df = rsi_df.mask(rsi_df<65, 0)
#END RSI(14) ABOVE 60
#END RSI(14) ABOVE 60
#END RSI(14) ABOVE 60



#START AVERAGE STOCHRSI ABOVE 95
#START AVERAGE STOCHRSI ABOVE 95
#START AVERAGE STOCHRSI ABOVE 95
list7 = []
stoch_rsi_d_df = pd.DataFrame(list7)

for i in adj_close_df:
    indicator_stochrsi = StochRSIIndicator(close=adj_close_df[i], window=14, smooth1=3, smooth2=3, fillna=False)
    stoch_rsi_d_df[i] = indicator_stochrsi.stochrsi_d()


list8 = []
stoch_rsi_k_df = pd.DataFrame(list8)

for i in adj_close_df:
    indicator_stochrsi = StochRSIIndicator(close=adj_close_df[i], window=14, smooth1=3, smooth2=3, fillna=False)
    stoch_rsi_k_df[i] = indicator_stochrsi.stochrsi_k()


stoch_rsi_d_df = stoch_rsi_d_df*100
stoch_rsi_k_df = stoch_rsi_k_df*100

stoch_rsi_avg = (stoch_rsi_d_df + stoch_rsi_k_df)/2

stoch_rsi_avg = stoch_rsi_avg.mask(stoch_rsi_avg>=97, 104)
stoch_rsi_avg = stoch_rsi_avg.mask(stoch_rsi_avg<104, 0)
#END AVERAGE STOCHRSI ABOVE 95
#END AVERAGE STOCHRSI ABOVE 95
#END AVERAGE STOCHRSI ABOVE 95

sell_sig_df = diff_close_25std_df + rsi_df + stoch_rsi_avg
sell_sig_df = sell_sig_df.mask(sell_sig_df<50, 0)

#END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL
#END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL
#END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL - END SELL SIGNAL




#START PREP BACKTESTING DATA
#START PREP BACKTESTING DATA
#START PREP BACKTESTING DATA
list15 = []
backtesting_df = pd.DataFrame(list15)

for i in adj_close_df:
    backtesting_df[i + '_BUY'] = buy_sig_df[i]
    backtesting_df[i + '_SELL'] = sell_sig_df[i]
    backtesting_df[i + '_OPEN'] = open_df[i]
    backtesting_df[i + '_RETURN'] = ""
#END PREP BACKTESTING DATA
#END PREP BACKTESTING DATA
#END PREP BACKTESTING DATA



backtesting_df
