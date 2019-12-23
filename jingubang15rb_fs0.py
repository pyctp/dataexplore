'''

VARIABLE:SS:=0;

TT:VALUEWHEN(CROSSDOWN(BKVOL,0.5)||CROSSDOWN(SKVOL,0.5),MONEYTOT),NODRAW;

IF BARPOS=1 THEN
SS:=1;

IF MONEYTOT>HV(TT,0)&&BKVOL+SKVOL=0 THEN
SS:=1;

IF (CROSSDOWN(BKVOL,0.5)||CROSSDOWN(SKVOL,0.5))&&MONEYTOT<=HV(TT,0) THEN
SS:=SS+1;
MM:SS,NODRAW, COLorYELLOW;

//以上是资金管理模块

KNUM:=COUNT(C>0,0);
初始:REF(MONEYREAL/10000,KNUM-1),NODRAW;
当前..MONEYREAL/10000,COLorCYAN;
QYMA..EMA(当前, 12),COLorYELLOW,LINETHICK3;
最小..LV(当前,0);
最大..HV(当前,0),COLorGREEN,LINETHICK3;

DANGRI:=BARSLAST(DATE<>REF(DATE,1));

FANSHOU:=0;
QBP:=LASTSIG=201;
QBK:=LASTSIG<>201;
QSP:=LASTSIG=200;
QSK:=LASTSIG<>200;

RSV:=(C-LLV(L,63))/(HHV(H,63)-LLV(L,63))*100;
K:=SMA(RSV,18,1);
MAA:=EMA(C,255);
AA:=ABS(C-REF(C,1))>=REF(HHV(ABS(H-L),35),1);
AA2:=ABS(C-REF(C,2))>=REF(HHV(ABS(C-REF(C,2)),35),1);


 (C_MAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and FANSHOU=0 and QBP,BP(SKVOL);
 (C_MAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and FANSHOU=0 and QBK,BK(SS);
 (C_MAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and FANSHOU=1,BPK(SS);
 (CsMAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and QBP,BP(SKVOL);

 (CsMAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and FANSHOU=0 and QSP,SP(BKVOL);
 (CsMAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and FANSHOU=0 and QSK,SK(SS);
 (CsMAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and FANSHOU=1,SPK(SS);
 (C_MAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and QSP,SP(BKVOL);

TMP:=STD(O+C,93)/2;
OO:=VALUEWHEN(DATE<>REF(DATE,1),O);
CC:=VALUEWHEN(DATE<>REF(DATE,1),C);
BB:=MAX(OO,CC)+0.1*5*TMP;
DD:=MIN(OO,CC)-0.1*5*TMP;

 (C_MAA.iloc[i] and K<48 and C>REF(C,1) and (C>BB and C>SKPRICE)) and FANSHOU=0 and QBP,BP(SKVOL);
 (C_MAA.iloc[i] and K<48 and C>REF(C,1) and (C>BB and C>SKPRICE)) and FANSHOU=0 and QBK,BK(SS);
 (C_MAA.iloc[i] and K<48 and C>REF(C,1) and (C>BB and C>SKPRICE)) and FANSHOU=1,BPK(SS);

 (CsMAA.iloc[i] and K>39 and C<REF(C,1) and (C<DD and C<BKPRICE)) and FANSHOU=0 and QSP,SP(BKVOL);
 (CsMAA.iloc[i] and K>39 and C<REF(C,1) and (C<DD and C<BKPRICE)) and FANSHOU=0 and QSK,SK(SS);
 (CsMAA.iloc[i] and K>39 and C<REF(C,1) and (C<DD and C<BKPRICE)) and FANSHOU=1,SPK(SS);

RC:=C/REF(C,1);
ARC:=SMA(REF(RC,1),177,1);
MA1:=MA(C,85);
MA2:=MA(C,190);

 (CROSS(MA1,MA2) and ARC>1) and FANSHOU=0 and QBP,BP(SKVOL);
 (CROSS(MA1,MA2) and ARC>1) and FANSHOU=0 and QBK,BK(SS);
 (CROSS(MA1,MA2) and ARC>1) and FANSHOU=1,BPK(SS);
 (CROSS(MA2,MA1) and ARC<1) and FANSHOU=0 and QSP,SP(BKVOL);
 (CROSS(MA2,MA1) and ARC<1) and FANSHOU=0 and QSK,SK(SS);
 (CROSS(MA2,MA1) and ARC<1) and FANSHOU=1,SPK(SS);

VAR1:=(2*C+H+L)/4;
VAR2:=LLV(L,63);
VAR3:=HHV(H,63);
ZL:=EMA((VAR1-VAR2)/(VAR3-VAR2)*100,373);
SH:=EMA(0.7*REF(ZL,1)+0.3*ZL,118);

 (CROSS(ZL,SH) and SH>54) and FANSHOU=0 and QBP,BP(SKVOL);
 (CROSS(ZL,SH) and SH>54) and FANSHOU=0 and QBK,BK(SS);
 (CROSS(ZL,SH) and SH>54) and FANSHOU=1,BPK(SS);
 (CROSS(SH,ZL) and ZL<45) and FANSHOU=0 and QSP,SP(BKVOL);
 (CROSS(SH,ZL) and ZL<45) and FANSHOU=0 and QSK,SK(SS);
 (CROSS(SH,ZL) and ZL<45) and FANSHOU=1,SPK(SS);
 (CROSS(ZL,SH) and SH<48) and FANSHOU=0 and QBP,BP(SKVOL);
 (CROSS(ZL,SH) and SH<48) and FANSHOU=0 and QBK,BK(SS);
 (CROSS(ZL,SH) and SH<48) and FANSHOU=1,BPK(SS);
 (CROSS(SH,ZL) and ZL>72) and FANSHOU=0 and QSP,SP(BKVOL);
 (CROSS(SH,ZL) and ZL>72) and FANSHOU=0 and QSK,SK(SS);
 (CROSS(SH,ZL) and ZL>72) and FANSHOU=1,SPK(SS);

MAB:=EMA(C,109);
RSV2:=(C-LLV(L,3))/(HHV(H,3)-LLV(L,3))*100;
KK:=SMA(RSV2,59,1);
DD2:=SMA(KK,105,1);

 (CROSS2(KK,DD2,214) and DD2<1 and MAB>REF(MAB,1)) and FANSHOU=0 and QBP,BP(SKVOL);
 (CROSS2(KK,DD2,214) and DD2<1 and MAB>REF(MAB,1)) and FANSHOU=0 and QBK,BK(SS);
 (CROSS2(KK,DD2,214) and DD2<1 and MAB>REF(MAB,1)) and FANSHOU=1,BPK(SS);
 (CROSS2(DD2,KK,214) and DD2>47 and MAB<REF(MAB,1)) and FANSHOU=0 and QSP,SP(BKVOL);
 (CROSS2(DD2,KK,214) and DD2>47 and MAB<REF(MAB,1)) and FANSHOU=0 and QSK,SK(SS);
 (CROSS2(DD2,KK,214) and DD2>47 and MAB<REF(MAB,1)) and FANSHOU=1,SPK(SS);

 C<(1-0.001*34)*BKPRICE,SP(BKVOL);
 C>(1+0.001*48)*SKPRICE,BP(SKVOL);
 C>(1+0.001*272)*BKPRICE,SP(BKVOL);
 C<(1-0.001*95)*SKPRICE,BP(SKVOL);

SETSIGPRICETYPE(BK,LIMIT_orDER);
SETSIGPRICETYPE(SK,LIMIT_orDER);
SETSIGPRICETYPE(BP,LIMIT_orDER);
SETSIGPRICETYPE(SP,LIMIT_orDER);
SETSIGPRICETYPE(BPK,LIMIT_orDER);
SETSIGPRICETYPE(SPK,LIMIT_orDER);
SETSIGPRICETYPE(CLOSEOUT,LIMIT_orDER);

SIGNOW..LASTSIG,NODRAW;


/*
LASTSIG判断最近一个信号

注：由BPK指令产生的BK信号按BPK信号处理，SPK指令产生的SK信号同理。

例：AA:LASTSIG=BK;//最近一个 稳定的信号为BK信号AA返回值为1，否则返回0.
LASTSIG的不同返回值代表的信号：
BK:200;
SK:201;
BP:202;
SP:203;
BPK:204;
SPK:205;
CLOSEOUT:206;
STOP:207;
//TRADE_OTHER('AUTO');

//行情中寻找阶段高低点，在低点进场做多，高点进场做空，但是这些高低点都是波浪的一浪和二浪的回撤低点，不是逆势接单。下单采用市价，不用客户自己设置成交点位，程序会自动换月，需要把螺纹指数和螺纹主力的15分钟数据下载完全，加载到螺纹15分指数上。
'''

from datetime import time, datetime
# from LogEngine import LogEngine
import datetime
import pandas as pd
from datetime import date
from tqsdk import TqApi, TqSim, TqAccount, TargetPosTask, TqBacktest
from tqsdk.tafunc import (hhv, llv, ma, crossup, crossdown, median, harmean, sma, ema, abs, std, ref, exist, every, time_to_str)
# from myfunction import HHV, LLV, cross3, cross3down, MID, HLV, CROSS, cross
from pprint import pprint
import datetime
from time import sleep

# SYMBOL = "CZCE.TA909"
# SYMBOL = "CZCE.SR909"
SYMBOL = "SHFE.rb2005"
# SYMBOL = "DCE.pp2001"
# SYMBOL = "DCE.i2001"

symname = SYMBOL.split('.')[1]

# api = TqApi(TqAccount("H海通期货", "320102", "123456"))
# from tradefuncs import *
# acc = TqSim(150000)
# api = TqApi(acc)
# api = TqApi(acc, backtest=TqBacktest(start_dt=date(2019, 8, 26), end_dt=date(2019, 12, 9)))  # 回测
# api = TqApi(TqAccount("C创元期货", '11009312', 'Qiai1301'))
SS = 1
api = 0

lastsig = []
sigall = []



def BK(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='BUY', offset='OPEN', limit_price=order_price, volume=volume)


def SP(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='SELL', offset='CLOSE', limit_price=order_price, volume=volume)


def SK(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='SELL', offset='OPEN', limit_price=order_price, volume=volume)


def BP(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='BUY', offset='CLOSE', limit_price=order_price, volume=volume)


def BPK(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='BUY', offset='CLOSE', limit_price=order_price, volume=volume)
    api.insert_order(api, SYMBOL, direction='BUY', offset='OPEN', limit_price=order_price, volume=volume)

def SPK(api=api, volume=SS):
    order_price = quote.last_price
    api.insert_order(api, SYMBOL, direction='SELL', offset='CLOSE', limit_price=order_price, volume=volume)
    api.insert_order(api, SYMBOL, direction='SELL', offset='OPEN', limit_price=order_price, volume=volume)

def BARSSK():
    if lastsig and lastsig[-1] == 'SK':
        if sigall[-1] == 'SK':
            ret = 0
        else:
            ret = sigall[-1]
    else:
        ret = 0
    return ret


def BARSBK():
    if lastsig and lastsig[-1] == 'BK':
        if sigall[-1] == 'BK':
            ret = 0
        else:
            ret = sigall[-1]
    else:
        ret = 0

    return ret

def BARSBP():
    if lastsig and lastsig[-1] == 'BP':
        if sigall[-1] == 'BP':
            ret = 0
        else:
            ret = sigall[-1]

    else:
        ret = 0

    return ret


def BARSSP():
    if lastsig and lastsig[-1] == 'SP':
        if sigall[-1] == 'SP':
            ret = 0
        else:
            ret = sigall[-1]

    else:
        ret = 0

    return ret


def getLastSig():
    if lastsig:
        return lastsig[-1]
    else:
        return None


# account = api.get_account()
# position = api.get_position(SYMBOL)
# ticks = api.get_tick_serial(SYMBOL)
# klines900 = api.get_kline_serial(SYMBOL, duration_seconds=900, data_length=8964)
# bars = klines900.dropna()

bars = pd.read_csv(r'd:\ctplrn\ta\rb.csv')

# rs = bars.set_index('datetime')

# bars.datetime = bars.datetime.map(lambda x: time_to_str(x))

# bars.datetime = pd.to_datetime(bars.datetime)
bars.rename(columns={'KQ.i@SHFE.rb.open':'open', 'KQ.i@SHFE.rb.high':'high', 'KQ.i@SHFE.rb.low':'low', 'KQ.i@SHFE.rb.close':'close'}, inplace = True)

import json

def getDayFirstBarOC(bars):
    # 注意K线更新时需要更新
    oolist = []
    cclist = []
    for i in range(len(bars)):
        if i <= 3:
            OO = bars.iloc[0].open
            CC = bars.iloc[0].close
            oolist.append(OO)
            cclist.append(CC)

        if i > 3:
            # print(str(bars.iloc[i-3].datetime).split(' ')[0])
            # print(str(bars.iloc[i-2].datetime).split(' ')[0])
            if str(bars.iloc[i-2].datetime).split(' ')[0] != str(bars.iloc[i-3].datetime).split(' ')[0]:
                OO = bars.iloc[i-2].open
                CC = bars.iloc[i-2].close
                oolist.append(OO)
                cclist.append(CC)
            else:
                OO = oolist[-1] # 这样对吗?
                CC = cclist[-1]
                oolist.append(OO)
                cclist.append(CC)


    oojson = json.dumps(oolist)
    ccjson = json.dumps(cclist)
    with open('oolist.json', 'w') as f:
        json.dump(oojson, f)

    with open('cclist.json', 'w') as f:
        json.dump(ccjson, f)

    return oolist, cclist




# daybar = api.get_kline_serial(SYMBOL, duration_seconds=60 * 60 * 24, data_length=100)

# dayopen = daybar.iloc[i].open
# dayhl = daybar.dropna().high - daybar.dropna().low
# avghl = dayhl.tolist()[-5:]
# meanhl = median(dayhl, len(dayhl)).iloc[i]
# mahl = ma(dayhl, 12).iloc[i]
# maxhl = max(dayhl)
# minhl = min(dayhl)
##
# quote = api.get_quote(SYMBOL)
# lastprice = quote.last_price


SS = 1


# LASTSIG = getLastSig()

# DANGRI:=BARSLAST(DATE<>REF(DATE,1));

FANSHOU = 0
SS = 1
# BKVOL = api.get_position(SYMBOL).volume_long
# SKVOL = api.get_position(SYMBOL).volume_short


# QBP = LASTSIG == 201  #SK
# QBK = LASTSIG != 201  #SK
# QSP = LASTSIG == 200  #BK
# QSK = LASTSIG != 200  #BK

'''LASTSIG判断最近一个信号
注：由BPK指令产生的BK信号按BPK信号处理，SPK指令产生的SK信号同理。

例：AA:LASTSIG=BK;//最近一个 稳定的信号为BK信号AA返回值为1，否则返回0.
LASTSIG的不同返回值代表的信号：
BK:200;
SK:201;
BP:202;
SP:203;
BPK:204;
SPK:205;
CLOSEOUT:206;
STOP:207;
'''
lastsig = []
sigall = []

def jingubang(bars):
    global lastsig, sigall

    O = bars.open
    H = bars.high
    L = bars.low
    C = bars.close

    ISUP = bars.open >= bars.close
    ISDOWN = bars.open < bars.close


    # 计算rsv， maa 等第一部分数据
    RSV = (C - llv(L, 63)) / (hhv(H, 63) - llv(L, 63)) * 100
    K = sma(RSV, 18, 1)
    MAA = ema(C, 255)
    AA = abs(C - ref(C, 1)) >= ref(hhv(abs(H - L), 35), 1)
    AA2 = abs(C - ref(C, 2)) >= ref(hhv(abs(C - ref(C, 2)), 35), 1)

    C_MAA = C > MAA
    CbMAA = C > MAA
    CsMAA = C < MAA
    CbREFC = C > ref(C, 1)
    CsREFC = C < ref(C, 1)


    # 计算第二部分数据
    # OOlist, CClist = getDayFirstBarOC(bars)
    with open('oolist.json', 'r') as f:
        list = json.load(f)
        OOlist = eval(list)

    with open('cclist.json', 'r') as f:
        list = json.load(f)
        CClist = eval(list)

    TMP = std(O + C, 93) / 2

    for i in range(len(O)):

        tmp = TMP.iloc[i]
        # print(tmp, type(tmp), str(tmp))
        if str(tmp) == 'nan':
            continue

        OO = OOlist[i]
        CC = CClist[i]
        BB = max(OO, CC) + 0.1 * 5 * tmp
        DD = min(OO, CC) - 0.1 * 5 * tmp
        CbBB = C > BB
        CsDD = C < DD

    # 计算第三部分数据
    sigall = []
    RC = C / ref(C, 1)
    ARC = sma(ref(RC, 1), 177, 1)
    MA1 = ma(C, 85)
    MA2 = ma(C, 190)
    CROSSUPMA1MA2 =crossup(MA1, MA2)
    CROSSDOWNMA1MA2 = crossdown(MA1, MA2)


    # 计算第四部分数据
    VAR1 = (2 * C + H + L) / 4
    VAR2 = llv(L, 63)
    VAR3 = hhv(H, 63)
    ZL = ema((VAR1 - VAR2) / (VAR3 - VAR2) * 100, 373)
    SH = ema(0.7 * ref(ZL, 1) + 0.3 * ZL, 118)

    CROSSUPZLSH = crossup(ZL, SH)
    CROSSDOWNZLSH = crossdown(ZL, SH)


    # 计算第五部分数据
    MAB = ema(C, 109)
    RSV2 = (C - llv(L, 3)) / (hhv(H, 3) - llv(L, 3)) * 100
    KK = sma(RSV2, 59, 1)
    DD2 = sma(KK, 105, 1)

    MABbREF1 = MAB > ref(MAB,1)
    MABsREF1 = MAB < ref(MAB,1)

    CROSS_KK_up_DD2 = crossup(KK, DD2)
    CROSS_DD2_up_KK = crossup(DD2, KK)


    SKPRICE = []
    BKPRICE = []
    BPPRICE = []
    SPPRICE = []



    QBP = True
    QBK = True
    QSP = True
    QSK = True
    sigcount = 0

    # 开始计算信号
    for i in range(len(O)):

        if lastsig:
            QBP = lastsig[-1] == 'SK'
            QBK = lastsig[-1] != 'SK'
            QSP = lastsig[-1] == 'BK'
            QSK = lastsig[-1] != 'BK'
        else:
            QBP = True
            QBK = True
            QSP = True
            QSK = True


        print(BARSBK(), lastsig)
        # print(i, CbMAA.iloc[i], K.iloc[i],ISUP.iloc[i], AA.iloc[i], AA2.iloc[i])

        if (C_MAA.iloc[i] and K.iloc[i]<48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK()>109) and FANSHOU==0 and QBP:
            #     print('空单平仓。。。')
            #     BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0
        elif (C_MAA.iloc[i] and K.iloc[i] <48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK()>109) and FANSHOU==0 and QBK:
            #     BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0
        elif CsMAA.iloc[i] and K.iloc[i]<48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK()>109 and QBP:
            #     BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0
        #
        elif CsMAA.iloc[i] and K.iloc[i]>39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK()>50 and FANSHOU==0 and QSP:
            #     SP(BKVOL)
            lastsig.append('SP')
            sigall.append('BP')
            sigcount = 0
        elif (CsMAA.iloc[i] and K.iloc[i]>39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK()>50) and FANSHOU==0 and QSK:
            #     SK(SS)
            lastsig.append('SK')
            sigall.append('BP')
            sigcount = 0

       elif (C_MAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK()>50) and QSP:
            #     SP(BKVOL)
            lastsig.append('SP')
            sigall.append('BP')
            sigcount = 0

        # 第二段
        elif CbMAA.iloc[i] and K.iloc[i]<48 and CbREFC.iloc[i] and CbBB.iloc[i] and C.iloc[i] > SKPRICE and FANSHOU == 0 and  QBP:
            # BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0

        elif CbMAA.iloc[i] and K.iloc[i]<48 and CbREFC.iloc[i] and CbBB.iloc[i] and  C.iloc[i] > SKPRICE and FANSHOU == 0 and QBK:
            # BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0

        elif CbMAA.iloc[i] and K.iloc[i]>39 and CsREFC.iloc[i] and CsDD.iloc[i] and C.iloc[i] < BKPRICE and FANSHOU == 0 and  QSP:
            # SP(BKVOL)
            lastsig.append('SP')
            sigall.append('SP')
            sigcount = 0

        elif CsMAA.iloc[i] and K.iloc[i]>39 and CsREFC.iloc[i] and CsDD.iloc[i] and C.iloc[i] < BKPRICE and FANSHOU == 0 and  QSK:
            # SK(SS)
            lastsig.append('SK')
            sigall.append('SK')
            sigcount = 0

        # 第三段
        elif CROSSUPMA1MA2.iloc[i] and ARC.iloc[i] > 1 and FANSHOU == 0 and QBP:
            # BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0

        elif CROSSUPMA1MA2.iloc[i] and ARC.iloc[i] > 1 and FANSHOU == 0 and QBK:
            # BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0

        elif CROSSDOWNMA1MA2.iloc[i] and ARC.iloc[i] < 1 and FANSHOU == 0 and QSP:
            # SP(BKVOL)
            lastsig.append('SP')
            sigall.append('SP')
            sigcount = 0

        elif CROSSDOWNMA1MA2.iloc[i] and ARC.iloc[i] < 1 and FANSHOU == 0 and QSK:
            # SK(SS)
            lastsig.append('SK')
            sigall.append('SK')
            sigcount = 0

        # 第四段
        elif CROSSUPZLSH.iloc[i] and SH.iloc[i] > 54 and FANSHOU == 0 and QBP:
            # BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0


        elif CROSSUPZLSH.iloc[i] and SH.iloc[i] > 54 and FANSHOU == 0 and QBK:
            # BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0


        elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] <45 and FANSHOU == 0 and QSP:
            # SP(BKVOL)
            lastsig.append('SP')
            sigall.append('SP')
            sigcount = 0


        elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] <45 and FANSHOU == 0 and QSK:
            # SK(SS)
            lastsig.append('SK')
            sigall.append('SK')
            sigcount = 0



        elif CROSSUPZLSH.iloc[i] and SH.iloc[i] < 48 and FANSHOU == 0 and QBP:
            # BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0


        elif CROSSUPZLSH.iloc[i] and SH.iloc[i] < 48 and FANSHOU == 0 and QBK:
            # BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0


        elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] >72 and FANSHOU == 0 and QSP:
            # SP(BKVOL)
            lastsig.append('SP')
            sigall.append('SP')
            sigcount = 0


        elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] >72 and FANSHOU == 0 and QSK:
            # SK(SS)
            lastsig.append('SK')
            sigall.append('SK')
            sigcount = 0


        # 第五段
        elif CROSS_KK_up_DD2.iloc[i] and DD2.iloc[i] < 1 and MABbREF1.iloc[i] and FANSHOU == 0 and QBP:
            # BP(SKVOL)
            lastsig.append('BP')
            sigall.append('BP')
            sigcount = 0

        elif CROSS_KK_up_DD2.iloc[i] and DD2.iloc[i] < 1 and MABbREF1.iloc[i] and FANSHOU == 0 and QBK:
            # BK(SS)
            lastsig.append('BK')
            sigall.append('BK')
            sigcount = 0

        elif CROSS_DD2_up_KK.iloc[i] and DD2.iloc[i] > 47 and MABsREF1.iloc[i] and FANSHOU == 0 and QSP:
            # SP(BKVOL)
            lastsig.append('SP')
            sigall.append('SP')
            sigcount = 0

        elif CROSS_DD2_up_KK.iloc[i] and DD2.iloc[i] > 47 and MABsREF1.iloc[i] and FANSHOU == 0 and QSK:
            # SK(SS)
            lastsig.append('SK')
            sigall.append('SK')
            sigcount = 0


        else:
            sigcount += 1
            sigall.append(sigcount)

    print('end.....')
    print('sss')

    '''
CROSS2(A,B,N) 表示N个周期内当A从下方向上穿B偶数次。

注：
1、若N为0，则从第一个有效的值开始算。
2、当N为有效值，但当前的k线数不足N根，或者N空值的情况下，代表不成立，该函数返回0
3、N可以为变量

例1：
MA5:=MA(C,5);
CROSS2(C,MA5,10) 返回值为1(Yes)，表示当前周期是10个周期内(包含当前周期)收盘价从下方向上穿过5周期均线的第偶数次；返回值为0(No)，表示当前周期不是10个周期内(包含当前周期)收盘价从下方向上穿过5周期均线的第偶数次

'''

while True:
    # api.wait_update()

    jingubang(bars)


