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
print(len(sigprice), sigprice)
# print(sigall)
profit = 0
profitlist = []
profittmplist = []

for i in range(len(lastsig)):
    if i == 0:
        continue

    else:
        if lastsig[i] == 'bpk':
            pricebk = sigprice[i]
            profittmp = sigprice[i-1] - sigprice[i]
            profit += profittmp
        if lastsig[i] == 'spk':
            pricesk = sigprice[i]
            profittmp = sigprice[i] - sigprice[i-1]
            profit += profittmp
        print(profit, profittmp)
        profitlist.append(profit)
        profittmplist.append(profittmp)

print(profit)
bg0 = []
sm0 = []
for i in range(len(profittmplist)):
    if profittmplist[i]>=0:
        bg0.append(profittmplist[i])
    else:
        sm0.append(profittmplist[i])
print(len(bg0), len(sm0), len(profittmplist))
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
