# coding:utf-8
import pandas as pd
from wavefunc2 import *
# bars = pd.read_csv('kline.csv')
# bars.rename(columns={"SHFE.rb2005.open":"open","SHFE.rb2005.high":"high","SHFE.rb2005.low":"low","SHFE.rb2005.close":"close"},inplace=True)
# bars.to_json('bars.json')


bars = pd.read_json('bars.json')

k2, g = get_WaveTrader(bars)

lastsig, sigprice, sigall = gen_wave_signals(k2, bars)

print(k2)
print(len(lastsig), lastsig)
print(sigprice)
print(sigall)
#
# for i in range(len(bars)):
#
#     bar = bars.iloc[:i]
#     if bar.empty:
#         continue
#
#     # print(bar)
#     # print('-'*10)
#     k2, g = get_WaveTrader(bar)
#
#     lastsig, sigprice, sigall = gen_wave_signals(k2, bar)
#
#     print(k2)
#     print(lastsig)
#     print(sigprice)
#     print(sigall)
