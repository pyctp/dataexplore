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


#

def getDayFirstBarOC(bars):
    # 获得交易日第一根k的开盘价和收盘价序列.
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
                # print(bars.iloc[i].datetime)
                OO = bars.iloc[i].open
                CC = bars.iloc[i].close
                oo = oo.append({'datetime': bars.iloc[i].datetime, 'OO': OO}, ignore_index=True)
                cc = cc.append({'datetime': bars.iloc[i].datetime, 'CC': CC}, ignore_index=True)

            else:
                OO = oo.iloc[-1].OO  #
                CC = cc.iloc[-1].CC
                oo = oo.append({'datetime': bars.iloc[i].datetime, 'OO': OO}, ignore_index=True)
                cc = cc.append({'datetime': bars.iloc[i].datetime, 'CC': CC}, ignore_index=True)

    # 计算结果保存到json文件中.
    oo.to_json('oo.json')
    cc.to_json('cc.json')
    return oo, cc


# 计算第一部分数据
llv63 = pd.Series(LLV(L,63))
hhv63 = pd.Series(HHV(H,63))
hhvhl35 = pd.Series(HHV(H-L,35))
hhvc_c35 = pd.Series(HHV(abs(C-ref(C,2)),35))

RSV = (C - llv63) / (hhv63 - llv63) * 100
K = sma(RSV, 18, 1)
MAA = ema(C, 255)
AA = abs(C-ref(C,1)) >= ref(hhvhl35,1)
AA2 = abs(C-ref(C,2)) >= ref(hhvc_c35,1)

CbMAA = C > MAA
CsMAA = C < MAA
CbREFC = C > ref(C, 1)
CsREFC = C < ref(C, 1)


# 计算第二部分数据
# OO, CC = getDayFirstBarOC(bars)

TMP = std(O + C, 93) / 2

oo = pd.read_json('oo.json')
cc = pd.read_json('cc.json')

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

# 计算第三部分数据
RC = C / ref(C, 1)
ARC = sma(ref(RC, 1), 177, 1)
MA1 = ma(C, 85)
MA2 = ma(C, 190)
CROSSUPMA1MA2 = crossup(MA1, MA2)
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

MABbREF1 = MAB > ref(MAB, 1)
MABsREF1 = MAB < ref(MAB, 1)

CROSS_KK_up_DD2 = crossup(KK, DD2)
CROSS_DD2_up_KK = crossup(DD2, KK)

print('数据计算完毕...')

# 信号计算部分


if (C_MAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK() > 109) and FANSHOU == 0 and QBP:
    #     print('空单平仓。。。')
    #     BP(SKVOL)
    lastsig.append('BP')
    sigall.append('BP')
    sigcount = 0
elif (C_MAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK() > 109) and FANSHOU == 0 and QBK:
    #     BK(SS)
    lastsig.append('BK')
    sigall.append('BK')
    sigcount = 0
elif C_MAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK() > 109 and FANSHOU == 1:
    #     BPK(SS)
    lastsig.append('BPK')
    sigall.append('BP')
    sigcount = 0
elif CsMAA.iloc[i] and K.iloc[i] < 48 and ISUP.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSSK() > 109 and QBP:
    #     BP(SKVOL)
    lastsig.append('BP')
    sigall.append('BP')
    sigcount = 0
#
elif CsMAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK() > 50 and FANSHOU == 0 and QSP:
    #     SP(BKVOL)
    lastsig.append('SP')
    sigall.append('BP')
    sigcount = 0
elif (CsMAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK() > 50) and FANSHOU == 0 and QSK:
    #     SK(SS)
    lastsig.append('SK')
    sigall.append('BP')
    sigcount = 0

elif (CsMAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK() > 50) and FANSHOU == 1:
    #        SPK(SS)
    lastsig.append('SPK')
    sigcount = 0

elif (C_MAA.iloc[i] and K.iloc[i] > 39 and ISDOWN.iloc[i] and (AA.iloc[i] or AA2.iloc[i]) and BARSBK() > 50) and QSP:
    #     SP(BKVOL)
    lastsig.append('SP')
    sigall.append('BP')
    sigcount = 0

# 第二段
elif CbMAA.iloc[i] and K.iloc[i] < 48 and CbREFC.iloc[i] and CbBB.iloc[i] and C.iloc[i] > SKPRICE and FANSHOU == 0 and QBP:
    # BP(SKVOL)
    lastsig.append('BP')
    sigall.append('BP')
    sigcount = 0

elif CbMAA.iloc[i] and K.iloc[i] < 48 and CbREFC.iloc[i] and CbBB.iloc[i] and C.iloc[i] > SKPRICE and FANSHOU == 0 and QBK:
    # BK(SS)
    lastsig.append('BK')
    sigall.append('BK')
    sigcount = 0

elif CbMAA.iloc[i] and K.iloc[i] < 48 and CbREFC.iloc[i] and CbBB.iloc[i] and C.iloc[i] > SKPRICE and FANSHOU == 1:
    # BPK(SS)
    lastsig.append('BPK')
    sigall.append('BPK')
    sigcount = 0

elif CbMAA.iloc[i] and K.iloc[i] > 39 and CsREFC.iloc[i] and CsDD.iloc[i] and C.iloc[i] < BKPRICE and FANSHOU == 0 and QSP:
    # SP(BKVOL)
    lastsig.append('SP')
    sigall.append('SP')
    sigcount = 0

elif CsMAA.iloc[i] and K.iloc[i] > 39 and CsREFC.iloc[i] and CsDD.iloc[i] and C.iloc[i] < BKPRICE and FANSHOU == 0 and QSK:
    # SK(SS)
    lastsig.append('SK')
    sigall.append('SK')
    sigcount = 0

elif CsMAA.iloc[i] and K.iloc[i] > 39 and CsREFC.iloc[i] and CsDD.iloc[i] and C.iloc[i] < BKPRICE and FANSHOU == 1:
    # SPK(SS)
    lastsig.append('SPK')
    sigall.append('SPK')
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

elif CROSSUPMA1MA2.iloc[i] and ARC.iloc[i] > 1 and FANSHOU == 1:
    # BPK(SS)
    lastsig.append('BPK')
    sigall.append('BPK')
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

elif CROSSDOWNMA1MA2.iloc[i] and ARC.iloc[i] < 1 and FANSHOU == 1:
    # SPK(SS)
    lastsig.append('SPK')
    sigall.append('SPK')
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


elif CROSSUPZLSH.iloc[i] and SH.iloc[i] > 54 and FANSHOU == 1:
    # BPK(SS)
    lastsig.append('BPK')
    sigall.append('BPK')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] < 45 and FANSHOU == 0 and QSP:
    # SP(BKVOL)
    lastsig.append('SP')
    sigall.append('SP')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] < 45 and FANSHOU == 0 and QSK:
    # SK(SS)
    lastsig.append('SK')
    sigall.append('SK')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] < 45 and FANSHOU == 1:
    # SPK(SS)
    lastsig.append('SPK')
    sigall.append('SPK')
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


elif CROSSUPZLSH.iloc[i] and SH.iloc[i] < 48 and FANSHOU == 1:
    # BPK(SS)
    lastsig.append('BPK')
    sigall.append('BPK')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] > 72 and FANSHOU == 0 and QSP:
    # SP(BKVOL)
    lastsig.append('SP')
    sigall.append('SP')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] > 72 and FANSHOU == 0 and QSK:
    # SK(SS)
    lastsig.append('SK')
    sigall.append('SK')
    sigcount = 0


elif CROSSDOWNZLSH.iloc[i] and ZL.iloc[i] > 72 and FANSHOU == 1:
    # SPK(SS)
    lastsig.append('SPK')
    sigall.append('SPK')
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

elif CROSS_KK_up_DD2.iloc[i] and DD2.iloc[i] < 1 and MABbREF1.iloc[i] and FANSHOU == 1:
    # BPK(SS)
    lastsig.append('BPK')
    sigall.append('BPK')
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

elif CROSS_DD2_up_KK.iloc[i] and DD2.iloc[i] > 47 and MABsREF1.iloc[i] and FANSHOU == 1:
    # SPK(SS)
    lastsig.append('SPK')
    sigall.append('SPK')
    sigcount = 0

else:
    sigcount += 1
    sigall.append(sigcount)
