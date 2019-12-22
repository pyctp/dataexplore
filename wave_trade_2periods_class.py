#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 简单fairy 策略_fariy, v 0.2 tqsdk, class 版本
# 将高低点 改为 前一根k的开盘价和收盘价。
import threading
from tqsdk import TqApi, TqSim, TqAccount, TargetPosTask, TqBacktest
from tqsdk.tafunc import (hhv, llv, ma, crossup, crossdown, median, harmean)
from myfunction import HHV, LLV, cross3, cross3down, MID, HLV, CROSS, cross
from speaktext_nosound import speak_text
import datetime
from wavefunc2 import *
# from tradefuncs import display_acct_pos_info, display_all_positon
from tradefuncs import *
from pprint import pprint

def get_DayBarInfo(api, SYMBOL):
    daybar = api.get_kline_serial(SYMBOL, duration_seconds=60 * 60 * 24, data_length=360)
    dayhl = daybar.dropna().high - daybar.dropna().low
    meanhl = median(dayhl, len(dayhl)).iloc[-1]
    mahl = ma(dayhl, 12).iloc[-1]
    maxhl = max(dayhl)
    minhl = min(dayhl)
    return (meanhl, int(mahl), maxhl, minhl)



class wave2p(threading.Thread):
    def __init__(self, api, symbol, interval1=900, interval2=300, step=5, single_volume=1, bk_limit=1, sk_limit=1, zhisun=False):
        threading.Thread.__init__(self)
        # self.api = TqApi(TqAccount(acct.name, acct.investorid, acct.password))
        self.api = api
        self.symbol = symbol
        self.interval1 = interval1
        self.interval2 = interval2
        self.step = step
        self.single_volume = single_volume
        self.bk_limit = bk_limit
        self.sk_limit = sk_limit
        # self.trade_direction = trade_direction
        self.zhisun = zhisun


    def run(self):
        api = self.api
        interval1 = self.interval1
        interval2 = self.interval2
        symbol = self.symbol
        step = self.step

        single_volume = self.single_volume
        bk_limit = self.bk_limit
        sk_limit = self.sk_limit
        # trade_direction = self.trade_direction
        zhisun = self.zhisun

        quote = api.get_quote(symbol)
        price_tick = quote.price_tick
        volume_multiple = quote.volume_multiple
        price_decs = quote.price_decs

        SYMBOL = quote.underlying_symbol
        print(SYMBOL)
        symbolname = SYMBOL.rsplit('.', 1)[1]

        account = api.get_account()
        position = api.get_position(SYMBOL)
        order = api.get_order()
        trade = api.get_trade()

        bkvol = position.volume_long
        skvol = position.volume_short

        ticks = api.get_tick_serial(SYMBOL)
        quote = api.get_quote(SYMBOL)

        klines1 = api.get_kline_serial(SYMBOL, duration_seconds=interval1, data_length=30)
        klines2 = api.get_kline_serial(SYMBOL, duration_seconds=interval2, data_length=150)

        daybar = api.get_kline_serial(SYMBOL, duration_seconds=60 * 60 * 24, data_length=100)

        dayhl = daybar.dropna().high - daybar.dropna().low
        meanhl = median(dayhl, len(dayhl)).iloc[-1]
        mahl = ma(dayhl, 5).iloc[-1]
        maxhl = max(dayhl)
        minhl = min(dayhl)

        dayopen = daybar.iloc[-1].open

        daybarinfo = get_DayBarInfo(api, SYMBOL)
        meanhl = daybarinfo[0]

        top1 = dayopen + int(meanhl / 2)
        bot1 = dayopen - int(meanhl / 2)

        top2 = dayopen + meanhl
        bot2 = dayopen - meanhl

        lastprice = quote.last_price

        # print((datetime.datetime.fromtimestamp(klines1.iloc[-1]["datetime"] / 1e9)), L.iloc[-1], H.iloc[-1])
        print(datetime.datetime.fromtimestamp(klines1.iloc[-1]["datetime"] / 1e9))
        mylog.info(datetime.datetime.fromtimestamp(klines1.iloc[-1]["datetime"] / 1e9))
        # 计算15分钟周期信号
        (k2_1, g_1) = get_WaveTrader(klines1)
        (lastsig_1, sigprice_1, sigall_1) = gen_wave_signals(k2_1, klines1)

        # 计算5分钟周期信号
        (k2_2, g_2) = get_WaveTrader(klines2)
        (lastsig_2, sigprice_2, sigall_2) = gen_wave_signals(k2_2, klines2)

        orderlist = []

        bk_list = []
        sk_list = []
        sp_list = []
        bp_list = []

        # 日内多空盈亏统计
        day_buy_profits = 0
        day_sell_profits = 0

        grid = step * price_tick

        while True:
            api.wait_update()
            # 新交易日
            if api.is_changing(daybar.iloc[-1], "datetime"):
                print(datetime.datetime.fromtimestamp(daybar.iloc[-1]["datetime"] / 1e9))
                mylog.info(datetime.datetime.fromtimestamp(daybar.iloc[-1]["datetime"] / 1e9))
                dayopen = daybar.iloc[-1].open

                quote = api.get_quote(symbol)
                price_tick = quote.price_tick
                volume_multiple = quote.volume_multiple

                SYMBOL = quote.underlying_symbol
                print(SYMBOL)
                symbolname = SYMBOL.rsplit('.', 1)[1]

                account = api.get_account()
                position = api.get_position(SYMBOL)

                # 重置日内盈利初始值
                day_buy_profits = 0
                day_sell_profits = 0

                speak_text('新的一天到来了， 请注意开始交易。')
                print('新的一天到来了， 请注意开始交易。')

            # 判断最后一根K线的时间是否有变化，如果发生变化则表示新产生了一根K线

            # 15分钟周期相关处理
            if api.is_changing(klines1.iloc[-1], "datetime"):
                print(datetime.datetime.fromtimestamp(klines1.iloc[-1]["datetime"] / 1e9))
                mylog.info(datetime.datetime.fromtimestamp(klines1.iloc[-1]["datetime"] / 1e9))
                (k2_1, g_1) = get_WaveTrader(klines1)

                print(len(klines1), len(k2_1))
                if isinstance(sigall_1[-1], int):
                    sigcount_1 = sigall_1[-1]
                else:
                    sigcount_1 = 0

                print('15 min', sigall_1[-1])
                mylog.info('15 min', sigall_1[-1])
                print(k2_1, len(k2_1))

                if k2_1[-2] == 1 and k2_1[-1] == -3:
                    lastsig_1.append('bpk')
                    sigpricetmp = quote.last_price
                    sigprice_1.append(sigpricetmp)
                    sigall_1.append('bpk')
                    sigcount_1 = 0

                elif k2_1[-2] == -3 and k2_2[-1] == 1:
                    lastsig_1.append('spk')
                    sigpricetmp = quote.last_price
                    sigprice_1.append(sigpricetmp)

                    sigall_1.append('spk')
                    sigcount_1 = 0

                else:
                    sigcount_1 += 1
                    sigall_1.append(sigcount_1)

                # print(k2_1)
                print(sigall_1)
                # 根据条件开仓
                if sigall_1[-1] == 'bpk' and bkvol == 0:
                    BK(api, SYMBOL, quote, volume=single_volume)
                    mylog.info('BK', SYMBOL, quote.last_price, single_volume)
                if sigall_1[-1] == 'bpk' and skvol > 0:
                    BP(api,  SYMBOL, quote, volume=single_volume)
                    mylog.info('BP', SYMBOL, quote.last_price, single_volume)
                if sigall_1[-1] == 'spk' and skvol == 0:
                    SK(api, SYMBOL, quote, volume=single_volume)
                    mylog.info('SK', SYMBOL, quote.last_price, single_volume)
                if sigall_1[-1] == 'spk' and bkvol > 0:
                    SP(api, SYMBOL, quote, volume=single_volume)
                    mylog.info('SP', SYMBOL, quote.last_price, single_volume)
                # if k2[-1] == -3:
                #     zcyl = '止损:'
                #     floatprofit = quote.last_price - sigprice[-1]
                #     signal = '多'
                # elif k2[-1] == 1:
                #     zcyl = '止损:'
                #     floatprofit = sigprice[-1] - quote.last_price
                #     signal = '空'

                # datetime: 自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数
                # print('波段信号:', signal)
                display_all_positon(api)
                # display_acct_pos_info(api, SYMBOL)

            # 5分钟周期相关处理
            if api.is_changing(klines2.iloc[-1], "datetime"):
                print(datetime.datetime.fromtimestamp(klines2.iloc[-1]["datetime"] / 1e9))
                mylog.info(datetime.datetime.fromtimestamp(klines2.iloc[-1]["datetime"] / 1e9))
                (k2_2, g_2) = get_WaveTrader(klines2)

                if isinstance(sigall_2[-1], int):
                    sigcount_2 = sigall_2[-1]
                else:
                    sigcount_2 = 0

                if k2_2[-1] == -3 and k2_2[-2] == 1:
                    lastsig_2.append('bpk')
                    sigpricetmp = quote.last_price
                    sigprice_2.append(sigpricetmp)
                    sigall_2.append('bpk')
                    sigcount_2 = 0

                elif k2_2[-1] == 1 and k2_2[-2] == -3:
                    lastsig_2.append('spk')
                    sigpricetmp = quote.last_price
                    sigprice_2.append(sigpricetmp)

                    sigall_2.append('spk')
                    sigcount_2 = 0

                else:
                    sigcount_2 += 1
                    sigall_2.append(sigcount_2)

                print('5 min', sigall_2[-1])
                mylog.info('5 min', sigall_2[-1])
                # 15 分钟周期多头
                if lastsig_1[-1] == 'bpk':
                    if sigall_2[-1] == 'spk' and bkvol > 0:
                        SP(api,  SYMBOL, quote, single_volume)
                        mylog.info('SP', SYMBOL, quote.last_price, single_volume)
                    if sigall_2[-1] == 'bpk' and bkvol == 0:
                        BK(api,  SYMBOL, quote, volume=single_volume)
                        mylog.info('BK', SYMBOL, quote.last_price, single_volume)
                # 15 分钟空头
                elif lastsig_1[-1] == 'spk':
                    if sigall_2[-1] == 'bpk' and skvol > 0:
                        BP(api, SYMBOL, quote, single_volume)
                        mylog.info('BP', quote.last_price )
                    if sigall_2[-1] == 'spk' and skvol == 0:
                        SK(api, SYMBOL, quote, volume=single_volume)
                        mylog.info('SK', SYMBOL, quote.last_price, single_volume)

                # if k2_2[-1] == -3:
                #     zcyl = '止损:'
                #     floatprofit = quote.last_price - sigprice[-1]
                #     signal = '多'
                # elif k2_2[-1] == 1:
                #     zcyl = '止损:'
                #     floatprofit = sigprice[-1] - quote.last_price
                #     signal = '空'
                #

                # datetime: 自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数
                # print('波段信号:', signal)
                display_all_positon(api)
                # display_acct_pos_info(api, SYMBOL)


            # 判断整个tick序列是否有变化
            if api.is_changing(ticks) or api.is_changing(quote):
                # ticks.iloc[-1]返回序列中最后一个tick
                # print(("tick变化", ticks.iloc[-1]))
                tick = ticks.iloc[-1]
                tickprice = ticks.last_price
                ticklist = tickprice.tolist()

                dayopen = quote.open
                dayhigh = quote.highest
                daylow = quote.lowest
                zhenfu = dayhigh - daylow
                lastprice = quote.last_price
                dayvib = dayhigh - daylow

                try:
                    BB = (lastprice - daylow) / (dayhigh - daylow) if dayhigh != daylow else 0.5
                except:
                    BB = 0.5

                lastprice = quote.last_price

            if api.is_changing(trade):
                pprint(trade)
                # symbol_t = trade.instrument_id
                # direction = trade.direction
                # offset = trade.offset
                # volume = trade.volume
                # tradedatetime = trade.trade_date_time
                # userid = trade.user_id
                # fee = trade.commission
                # outs = "账号：%s，合约：%s，方向：%s，开平：%s,数量：%d，时间：%s，手续费：%d"
                # outdata = (userid, symbol_t, direction, offset, volume, tradedatetime, fee)
                # print(outs%outdata)
                # , 'offset': 'OPEN', 'price': 7520.0, 'volume': 1, 'trade_date_time': 1576762191000000000, 'seqno': 25, 'user_id': '66882656', 'commission': 0.0}

            if api.is_changing(position):
                bkvol = position.volume_long
                skvol = position.volume_short

            if api.is_changing(account):
                moneyreal = account.balance


            for ord in bk_list:
                if ord.status == 'FINISHED':
                    order_price = ord.limit_price + grid
                    order = api.insert_order(SYMBOL, direction="SELL", offset="CLOSETODAY", volume=ord.volume_orign,
                                             limit_price=order_price)
                    sp_list.append(order)
                    bk_list.remove(ord)

                    speak_text(symbolname + '多单止盈单下单。')
                    print(order.instrument_id, '多单止盈单下单。', order_price)
                    mylog.info(order.instrument_id + '多单止盈单下单。' + str(order_price))

            for ord in sp_list:
                if ord.status == 'FINISHED':
                    day_buy_profits += ord.volume_orign * grid

                    speak_text(symbolname + '多单平仓完成。')

                    print(account.user_id, ord.instrument_id, '多单平仓完成', ord.limit_price, '日内空单盈利:', day_sell_profits, '日内多单盈利:', day_buy_profits)
                    sp_list.remove(ord)
                    up_trader_flag = True

            for ord in sk_list:
                if ord.status == 'FINISHED':
                    order_price = ord.limit_price - grid
                    order = api.insert_order(SYMBOL, direction="BUY", offset="CLOSETODAY", volume=ord.volume_orign,
                                             limit_price=order_price)
                    bp_list.append(order)
                    sk_list.remove(ord)
                    speak_text('空单平仓单下单。')
                    outs = order.instrument_id, '空单平仓单下单.', order_price
                    print(outs)
                    mylog.info(outs)

            for ord in bp_list:
                if ord.status == 'FINISHED':
                    day_sell_profits += ord.volume_orign * grid

                    speak_text(SYMBOL + '空单平仓完成。')
                    outs = account.user_id, ord.instrument_id, '空单平仓完成:', ord.limit_price, '日内空单盈利:', day_sell_profits, '日内多单盈利:', day_buy_profits
                    print(outs)
                    mylog.info(outs)
                    bp_list.remove(ord)
                    down_trader_flag = True

            # 多单止损

            if lastprice < dayopen and position.volume_long > 0 and zhisun:
                if sp_list:
                    for ord in sp_list:
                        api.cancel_order(ord)
                        sp_list.remove(ord)

                    order = api.insert_order(SYMBOL, direction='SELL', offset='CLOSE', limit_price=lastprice,
                                             volume=position.volume_long)

                    sp_list.append(order)
                    speak_text('多单止损下单。')

            # 空单止损

            if lastprice > dayopen and position.volume_short > 0 and zhisun:
                if bp_list:
                    for ord in bp_list:
                        api.cancel_order(ord)
                        bp_list.remove(ord)
                    order = api.insert_order(SYMBOL, direction='BUY', offset='CLOSE', limit_price=lastprice + 10,
                                             volume=position.volume_short)
                    sleep(1)

                    bp_list.append(order)
                    speak_text('空单止损下单。')


# 初始化策略参数
# 账号， 合约， 周期


if __name__=="__main__":

    import threading
    from loguru import logger as mylog

    from time import sleep
    #from accounts import cyzjy, tgjyzjy
    #acct = tgjyzjy

    mylog.add("sim_trading_{time}.log", rotation="20:55")

    symbols = ["KQ.m@CZCE.SR", "KQ.m@DCE.j", "KQ.m@SHFE.rb"]

    symboldict = {"nim": "KQ.m@SHFE.ni", "agm": "KQ.m@SHFE.ag", 'SRm': "KQ.m@CZCE.SR", 'jm': "KQ.m@DCE.j", 'rbm': "KQ.m@SHFE.rb", 'ppm': "KQ.m@DCE.pp"}

    # api_master = TqApi(TqAccount(acct.name, acct.investorid, acct.password))
    # api_master = TqApi(TqSim())

    # Create new threads
    # 可用参数: acct, symbol, interval = 300, step = 5, single_volume = 1, bk_limit = 1, sk_limit = 1, trade_direction = 'all', zhisun = False
    # thread1 = simple_fairy(cyzjy, "KQ.m@CZCE.SR", trade_direction='sell')
    mylog.info('策略启动。。。。')
    api = TqApi(TqSim(100000), backtest=TqBacktest(start_dt=datetime.date(2019, 12, 1), end_dt=datetime.date(2019, 12, 21)))  # 回测


    thread2 = wave2p(api, "KQ.m@SHFE.rb")
    # thread3 = simple_fairy(cyzjy, "KQ.m@SHFE.rb", trade_direction='all')

    # Start new Threads
    # thread1.start()
    thread2.start()
    # thread3.start()
    print('策略启动完成。')
    thread2.join()
