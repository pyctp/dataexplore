from tqsdk.tafunc import ref
import numpy as np

def get_HH1(H):
    H1 = ref(H, 1)
    H2 = ref(H, 2)
    hlist = H.tolist()
    h1list = H1.tolist()
    h2list = H2.tolist()
    HH1list = []

    for cc in range(len(hlist)):
        h = hlist[cc]
        h1 = h1list[cc]
        h2 = h2list[cc]

        if h < h1 and h1 < h2:
            HH1list.append(h2)
        else:
            HH1list.append(0)

    return HH1list


def get_LL1(L):
    # LL1:=IFELSE(L>REF(L,1)&&REF(L,1)>REF(L,2),REF(L,2),0);
    L1 = ref(L, 1)
    L2 = ref(L, 2)
    llist = L.tolist()
    l1list = L1.tolist()
    l2list = L2.tolist()

    LL1list = []

    for cc in range(len(llist)):
        l = llist[cc]
        l1 = l1list[cc]
        l2 = l2list[cc]
        if l > l1 and l1 > l2:
            LL1list.append(l2)
        else:
            LL1list.append(0)

    return LL1list


def get_HH2(HH1):
    # HH2: = VALUEWHEN(HH1 > 0, HH1);
    HH2list = []
    count = 0

    for cc in range(len(HH1)):
        hh1 = HH1[cc]

        if hh1 > 0:
            HH2list.append(hh1)
            count += 1

        elif count == 0:
            HH2list.append(None)

        elif count > 0:
            HH2list.append(HH2list[-1])

    return HH2list


def get_K1(C, HH2, LL2):
    # K1:=IFELSE(CLOSE>HH2,-3,IFELSE(CLOSE<LL2,1,0));
    closelist = C.tolist()

    K1list = []
    for cc in range(len(C)):
        hh2 = HH2[cc]
        close = closelist[cc]
        ll2 = LL2[cc]
        if hh2 is None or ll2 is None:
            K1list.append(None)
            continue

        if close > hh2:
            tmpk = -3
        else:
            if close < ll2:
                tmpk = 1
            else:
                tmpk = 0
        K1list.append(tmpk)

    return K1list


def get_K2(K1):
    # K2:=VALUEWHEN(K1<>0,K1);
    K2list = []
    count = 0
    for cc in range(len(K1)):
        k1 = K1[cc]
        if k1 is None:
            K2list.append(0)
            continue

        if k1 != 0:
            count += 1
            K2list.append(k1)

        elif count == 0:
            K2list.append(0)

        elif count > 0:
            K2list.append(K2list[-1])

    return K2list


def get_WaveTrader(bars):
    # bars 为tqsdk 返回的k线数据，格式为pandas的dataframe格式
    O = bars.open
    H = bars.high
    L = bars.low
    C = bars.close

    HH1 = get_HH1(H)
    HH2 = get_HH2(HH1)

    LL1 = get_LL1(L)
    LL2 = get_HH2(LL1)

    K1 = get_K1(C, HH2, LL2)
    K2 = get_K2(K1)

    G = get_G(K2, HH2, LL2)

    return K2, G



def get_G(K2, HH2, LL2):
    # G:IFELSE(K2=1,HH2,LL2)
    Glist = []
    for cc in range(len(K2)):
        k2 = K2[cc]
        hh2 = HH2[cc]
        ll2 = LL2[cc]

        if k2 == 1:
            tmpG = hh2
        else:
            tmpG = ll2

        Glist.append(tmpG)

    return Glist

def gen_wave_signals(k2, klines):
    #K2 为上面计算出来的列表

    lastsig = []
    lastsigdetail = []
    sigprice = []
    sigall = []
    sigcount = 0

    if not k2:
        return None
    else:

        for i in range(len(k2)):

            if i == 0 and k2[i] == -3:
                lastsig.append('bpk')
                sigpricetmp = klines.iloc[i].close
                sigprice.append(sigpricetmp)
                sigall.append('bpk')
                lastsigdetail.append((klines.iloc[i].datetime, 'bpk', klines.iloc[i].close))
            if i == 0 and k2[i] == 1:
                lastsig.append('spk')
                sigall.append('spk')
                sigpricetmp = klines.iloc[i].close
                sigprice.append(sigpricetmp)

                lastsigdetail.append((klines.iloc[i].datetime, 'spk', klines.iloc[i].close))
            else:
                pass

            if k2[i-1] != -3 and k2[i] == -3:
                lastsig.append('bpk')
                sigpricetmp = klines.iloc[i].close
                sigprice.append(sigpricetmp)
                sigall.append('bpk')
                lastsigdetail.append((klines.iloc[i].datetime, 'bpk', klines.iloc[i].close))
                sigcount = 0
            elif k2[i-1] != 1 and k2[i] == 1:
                lastsig.append('spk')
                sigpricetmp = klines.iloc[i].close
                sigprice.append(sigpricetmp)
                sigall.append('spk')
                lastsigdetail.append((klines.iloc[i].datetime, 'bpk', klines.iloc[i].close))
                sigcount = 0
            else:
                sigcount += 1
                sigall.append(sigcount)

    return lastsig, lastsigdetail, sigprice, sigall






def barssince(cond,n):
    '''
    第n个条件成立到当前的周期数.

    例：
        统计第一个条件(5周期上穿10周期)成立到当前的周期数：
        barssince = tafunc.barssince(tafunc.crossup(tafunc.ma(df['close'],5), tafunc.ma(df['close'],10)) , 1)

    注：
        1. 从当前k线开始算起
        2. n = 1,2,3 。。。。。

    '''
    total_length = len(cond)
    barssince_data = total_length - list(np.where(cond)[0])[n-1]

    return barssince_data
