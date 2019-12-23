import pandas as pd
import numpy as np
from tqsdk.tafunc import (hhv, llv, ma, sma, ema, crossup, crossdown, median, harmean, abs, std, ref, exist, every, time_to_str)
from myfunction import HHV, LLV
from datetime import date, datetime
bars = pd.read_json('rb2005_900.json')
O = bars.open
C = bars.close
H = bars.high
L = bars.low

# 交易日的问题

# 计算第四部分数据  处理完毕,基本正确
# VAR1 = (2 * C + H + L) / 4
# VAR2 = pd.Series(LLV(L, 63))
# VAR3 = pd.Series(HHV(H, 63))
#
# ZL = ema((VAR1 - VAR2) / (VAR3 - VAR2) * 100, 373)
# SH = ema(0.7 * ref(ZL, 1) + 0.3 * ZL, 118)
#


#
# TMP:=STD(O+C,93)/2
# OO:=VALUEWHEN(DATE<>REF(DATE,1),O)
# CC:=VALUEWHEN(DATE<>REF(DATE,1),C)
# BB:=MAX(OO,CC)+0.1*5*TMP
# DD:=MIN(OO,CC)-0.1*5*TMP


def getDayFirstBarOC(bars):
    # 注意K线更新时需要更新

    oo = pd.DataFrame(columns=('datetime', 'OO'))
    cc = pd.DataFrame(columns=('datetime', 'CC'))

    for i in range(len(bars)):
        if i == 0:
            OO = bars.iloc[0].open
            CC = bars.iloc[0].close
            oo = oo.append({'datetime': bars.iloc[0].datetime, 'OO': OO}, ignore_index=True)
            cc = cc.append({'datetime': bars.iloc[0].datetime, 'CC': CC}, ignore_index=True)

        else:
            hourtmp=bars.iloc[i].datetime.hour
            # daytmp=bars.iloc[i].datetime.day
            minutetmp=bars.iloc[i].datetime.minute
            # print(daytmp, hourtmp, minutetmp)
            #bars.iloc[i].datetime.day != bars.iloc[i-1].datetime.day
            if hourtmp == 21 and minutetmp == 0:
                print(bars.iloc[i].datetime)
                OO = bars.iloc[i].open
                CC = bars.iloc[i].close
                oo = oo.append({'datetime': bars.iloc[i].datetime, 'OO': OO}, ignore_index=True)
                cc = cc.append({'datetime': bars.iloc[i].datetime, 'CC': CC}, ignore_index=True)

            else:
                OO = oo.iloc[-1].OO  #
                CC = cc.iloc[-1].CC
                oo = oo.append({'datetime': bars.iloc[i].datetime, 'OO': OO}, ignore_index=True)
                cc = cc.append({'datetime': bars.iloc[i].datetime, 'CC': CC}, ignore_index=True)

    oo.to_json('oo.json')
    cc.to_json('cc.json')
    return oo, cc





# 计算第二部分数据
# OO, CC = getDayFirstBarOC(bars)

oo = pd.read_json('oo.json')
cc = pd.read_json('cc.json')

llv63 = pd.Series(LLV(L,63))
hhv63 = pd.Series(HHV(H,63))

RSV = (C - llv63) / (hhv63 - llv63) * 100
K = sma(RSV, 18, 1)
MAA = ema(C, 255)

CbMAA = C > MAA
CsMAA = C < MAA
CbREFC = C > ref(C, 1)
CsREFC = C < ref(C, 1)


TMP = std(O + C, 93) / 2

#
# bb = pd.Series()
# dd = pd.Series()
bb = []
dd = []
for i in range(len(bars)):

    tmp = TMP.iloc[i]
    # print(tmp, type(tmp), str(tmp))
    # print()
    # if tmp == np.nan:
    #     continue

    OO = oo.iloc[i].OO
    CC = cc.iloc[i].CC

    bbtmp = max(OO, CC) + 0.1 * 5 * tmp
    ddtmp = min(OO, CC) - 0.1 * 5 * tmp
    bb.append(bbtmp)
    dd.append(ddtmp)

BB = pd.Series(bb)
DD = pd.Series(dd)

CbBB = C > BB
CsDD = C < DD

bkprice = []
skprice = []


FANSHOU = 1
SKPRICE = 0
BKPRICE = 0
lastsig = []
sigall = []
sigcount = 0

# 计算信号
for i in range(len(bars)):

    if (CbMAA.iloc[i] and K.iloc[i] < 48 and CbREFC.iloc[i]) and (CbBB.iloc[i] and C.iloc[i] > SKPRICE):
        outs = bars.iloc[i].close, MAA.iloc[i], K.iloc[i], BB.iloc[i], TMP.iloc[i], oo.iloc[i], cc.iloc[i],
        # print(outs)
        # BPK(SS)
        lastsig.append([bars.iloc[i].datetime, 'BPK'])
        BKPRICE = bars.iloc[i].close
        bkprice.append(BKPRICE)
        sigall.append('BPK')
        sigcount = 0
        print(i, bars.iloc[i].datetime)


    elif (CsMAA.iloc[i] and K.iloc[i] > 39 and CsREFC.iloc[i]) and (CsDD.iloc[i] and C.iloc[i] < BKPRICE):
        # SPK(SS)
        lastsig.append([bars.iloc[i].datetime, 'SPK'])
        SKPRICE = bars.iloc[i].close
        skprice.append(SKPRICE)
        sigall.append('SPK')
        sigcount = 0
        print(i, bars.iloc[i].datetime)

    else:
        sigcount += 1
        sigall.append(sigcount)


print('   ')

 # (C>MAA AND K<48 AND C>REF(C,1) AND (C>BB AND C>SKPRICE)) AND FANSHOU=1,BPK(SS);
 #

 # (C<MAA AND K>39 AND C<REF(C,1) AND (C<DD AND C<BKPRICE)) AND FANSHOU=1,SPK(SS);