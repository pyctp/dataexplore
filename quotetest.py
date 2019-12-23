# coding:utf-8

from tqsdk import *
import pandas as pd
from wavefunc2 import *
symbol = 'CSI.000300'
api = TqApi()
quote = api.get_quote(symbol)
klines = api.get_kline_serial(symbol, duration_seconds=300)

while True:
    api.wait_update()
    if api.is_changing(quote):
        print(quote.last_price, quote.datetime, quote.underlying_symbol)

    if api.is_changing(klines.iloc[-1], 'datetime'):
        print(klines.iloc[-1])

def tq_bar_csv_to_json(csvfile):
    bars = pd.read_csv(csvfile, encoding='gbk')
    bars.rename(columns={"SHFE.rb2005.open": "open", "SHFE.rb2005.high": "high", "SHFE.rb2005.low": "low", "SHFE.rb2005.close": "close"}, inplace=True)
    jsonfile = csvfile.split('.')[0] + '.json'
    bars.to_json(jsonfile)


def tb_bar_csv_to_json(csvfile):
    barstb = pd.read_csv(csvfile, encoding='gbk')
    barstb.rename(columns={"时间": "datetime", "开盘价": "open", "最高价": "high", "最低价": "low", "收盘价": "close"}, inplace=True)
    jsonfile = csvfile.split('.')[0] + '.json'
    barstb.to_json(jsonfile)


# tq_bar_csv_to_json('rb2005_60.csv')
# tq_bar_csv_to_json('rb2005_300.csv')
# tq_bar_csv_to_json('rb2005_900.csv')
# tb_bar_csv_to_json('tbrb2005_5.csv')


barstq = pd.read_json('rb2005_300.json')
barstb = pd.read_json('tbrb2005_5.json')
print(len(barstq), len(barstb))


def compare_2_bars(bars1, bars2):
    length = min(len(bars1), len(bars2))
    time1list = bars1.datetime.to_list()
    time2list = bars2.datetime.to_list()
    count = 0
    for i in range(len(time1list)):
        if not time1list[i] in time2list:
            count += 1
            print(time1list[i], count)

    # for i in range(len(time2list)):
    #
    #     if not time2list[i] in time1list:
    #         count += 1
    #         print(time1list[i], count)
    #     print("now comparing:", i)
    for i in range(length):
        opent, hight, lowt, closet = bars1.iloc[i].open, bars1.iloc[i].high, bars1.iloc[i].low, bars1.iloc[i].close
        openb, highb, lowb, closeb = bars2.iloc[i].open, bars2.iloc[i].high, bars2.iloc[i].low, bars2.iloc[i].close
        # if not opent == openb:
        #     print(opent, openb, bars1.iloc[i].datetime, 'open diff', i)
        time1 = bars1.iloc[i].datetime
        time2 = bars2.iloc[i].datetime

        if time1 != time2:
            print('time diff:', time1, time2)
        else:
            continue

        if not hight == highb:
            print(hight, highb, bars1.iloc[i].datetime, 'high diff', i)
        # if not lowt == lowb:
        # print(lowt, lowb, bars1.iloc[i].datetime, 'low diff', i)
        # if not closet == closeb:
        #     print(opent, openb, bars1.iloc[i].datetime)


# compare_2_bars(barstq, barstb)
k2, g = get_WaveTrader(barstq)

lastsig, sigdetail, sigprice, sigall = gen_wave_signals(k2, barstq)

# wenhuasig = pd.read_csv('螺纹2005 15分钟 波段交易.csv', encoding='gbk')
wenhuasig = pd.read_csv('螺纹2005 5分钟 波段交易.csv', encoding='gbk')
diffsum = 0
for i in range(len(sigdetail)):
    price = sigdetail[i][2]
    whprice = wenhuasig.iloc[i].价格
    # print(sigdetail[i][0], price, whprice, price == whprice)
    tqtime = sigdetail[i][0]
    whtime = wenhuasig.iloc[i].时间.replace('/', '-', 2)
    tqtimen = str(tqtime)
    # print(tqtime, whtime)
    if tqtimen != whtime:
        print(tqtime, whtime, '..........................')
    # if price != whprice:
    #     print(sigdetail[i][0], wenhuasig.iloc[i].时间, price, whprice, price == whprice)
    #     print(price - whprice)
    #     diffsum += (price - whprice)
    # if price != wenhuasig.iloc[i+1].价格:
    #     print('price not equal....')

# print(diffsum)
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
            profittmp = sigprice[i - 1] - sigprice[i]
            profit += profittmp
        if lastsig[i] == 'spk':
            pricesk = sigprice[i]
            profittmp = sigprice[i] - sigprice[i - 1]
            profit += profittmp
        print(profit, profittmp)
        profitlist.append(profit)
        profittmplist.append(profittmp)

print(profit)
bg0 = []
sm0 = []
for i in range(len(profittmplist)):
    if profittmplist[i] >= 0:
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
