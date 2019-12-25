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
# 第一部分数据

# 第二部分数据, 完全正确

# 第三部分数据, 完全正确(修改了当日第一条k线判断为21:00的k线,加了信号过滤)
# TMP:=STD(O+C,93)/2
# OO:=VALUEWHEN(DATE<>REF(DATE,1),O)
# CC:=VALUEWHEN(DATE<>REF(DATE,1),C)
# BB:=MAX(OO,CC)+0.1*5*TMP
# DD:=MIN(OO,CC)-0.1*5*TMP


# 计算第四部分数据  处理完毕,基本正确
# VAR1 = (2 * C + H + L) / 4
# VAR2 = pd.Series(LLV(L, 63))
# VAR3 = pd.Series(HHV(H, 63))
#
# ZL = ema((VAR1 - VAR2) / (VAR3 - VAR2) * 100, 373)
# SH = ema(0.7 * ref(ZL, 1) + 0.3 * ZL, 118)
#

# 第一部分数据
# RSV:=(C-LLV(L,63))/(HHV(H,63)-LLV(L,63))*100;
# K:=SMA(RSV,18,1);
# MAA:=EMA(C,255);
# AA:=ABS(C-REF(C,1))>=REF(HHV(ABS(H-L),35),1);
# AA2:=ABS(C-REF(C,2))>=REF(HHV(ABS(C-REF(C,2)),35),1);

llv63 = pd.Series(LLV(L, 63))
hhv63 = pd.Series(HHV(H, 63))
hhvhl35 = pd.Series(HHV(H - L, 35))
c_refc2 = C - ref(C, 2)
abs_c_refc2 = abs(c_refc2)
tmp = HHV(abs_c_refc2, 35)
hhvc_c35 = pd.Series(HHV(abs_c_refc2, 35))

RSV = (C - llv63) / (hhv63 - llv63) * 100
K = sma(RSV, 18, 1)
MAA = ema(C, 255)
AA = abs(C - ref(C, 1)) >= ref(hhvhl35, 1)
AA2 = abs(C - ref(C, 2)) >= ref(hhvc_c35, 1)

C_MAA = C > MAA
CbMAA = C > MAA
CsMAA = C < MAA
CbREFC = C > ref(C, 1)
CsREFC = C < ref(C, 1)

ISUP = bars.open >= bars.close
ISDOWN = bars.open < bars.close
lastsig = []
sigall = []
sigcount = 0
bkprice = []
skprice = []



for i in range(len(bars)):

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


 # (C_MAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and FANSHOU=1,BPK(SS);
 # (CsMAA.iloc[i] and K<48 and ISUP and (AA or AA2) and BARSSK>109) and QBP,BP(SKVOL);
 #
 # (CsMAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and FANSHOU=1,SPK(SS);
 # (C_MAA.iloc[i] and K>39 and ISDOWN and (AA or AA2) and BARSBK>50) and QSP,SP(BKVOL);
 #
    print(bars.iloc[i].datetime, C_MAA.iloc[i], K.iloc[i], ISUP.iloc[i], AA.iloc[i], AA2.iloc[i])
    if C_MAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]):
        #     BPK(SS)
        if (not lastsig) or lastsig[-1][1] != 'BPK':
            lastsig.append([bars.iloc[i].datetime, 'BPK'])
            BKPRICE = bars.iloc[i].close
            bkprice.append(BKPRICE)


        sigall.append('BPK')
        sigcount = 0
    elif CsMAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]):
        #     BP(SKVOL)
        if (not lastsig) or lastsig[-1][1] != 'BP':
            lastsig.append([bars.iloc[i].datetime, 'BP'])
            BKPRICE = bars.iloc[i].close
            bkprice.append(BKPRICE)


        sigall.append('BP')
        sigcount = 0
        #

    elif (CsMAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i])):
        #        SPK(SS)
        if (not lastsig) or lastsig[-1][1] != 'SPK':
            lastsig.append([bars.iloc[i].datetime, 'SPK'])
            BKPRICE = bars.iloc[i].close
            bkprice.append(BKPRICE)

        sigall.append('SPK')
        sigcount = 0

    elif (C_MAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) ):
        #     SP(BKVOL)
        if (not lastsig) or lastsig[-1][1] != 'SP':
            lastsig.append([bars.iloc[i].datetime, 'SP'])
            BKPRICE = bars.iloc[i].close
            bkprice.append(BKPRICE)


        sigall.append('SP')
        sigcount = 0
    else:
        sigcount += 1
        sigall.append(sigcount)


print('end')