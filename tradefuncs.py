# coding: utf-8
# 交易相关的函数

def BK(api, symbol, quote,  volume):
    order_price = quote.last_price
    api.insert_order(symbol, direction='BUY',offset='OPEN', limit_price=order_price, volume=volume)

def SP(api, symbol, quote, volume):
    order_price = quote.last_price
    api.insert_order(symbol, direction='SELL', offset='CLOSE', limit_price=order_price, volume=volume)

def SK(api, symbol, quote, volume):
    order_price = quote.last_price
    api.insert_order(symbol, direction='SELL', offset='OPEN', limit_price=order_price, volume=volume)

def BP(api, symbol, quote, volume):
    order_price = quote.last_price
    api.insert_order(symbol, direction='BUY', offset='CLOSE', limit_price=order_price, volume=volume)

def BARSSK():
    pass


def BARSBK():
    pass


def BARSBP():
    pass


def BARSSP():
    pass


def getLastSig():
    pass


def display_acct_pos_info( symbol):
    position = api.get_position(symbol)
    account = api.get_account()
    print(account.user_id, symbol,  "净值: %.2f,可用: %.2f, 今多头: %d 手, 今空头: %d 手" % (account.balance, account.available, position.volume_long, position.volume_short))

def display_all_positon(api):
    position = api.get_position()
    for pos in position:
        # print(pos)
        if pos.split('.')[0] in ('CZCE', 'SHFE', 'DCE'):
            # print(position[pos])
            print(pos, '昨多:', position[pos]['pos_long_his'], '今多:', position[pos]['pos_long_today'])
            print(pos, '昨空:', position[pos]['pos_short_his'], '今空:', position[pos]['pos_short_today'])
