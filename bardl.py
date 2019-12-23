#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chengzhi'

from datetime import datetime
from contextlib import closing
from tqsdk import TqApi
from tqsdk.tools import DataDownloader

api = TqApi()
# 下载从 2018-01-01凌晨6点 到 2018-06-01下午4点 的 cu1805 分钟线数据
intervals =[60, 300, 900]
SYMBOL = "SHFE.rb2005"
symname = SYMBOL.split('.')[1]


for interval in intervals:
    filename = symname + '_' + str(interval) + '.csv'
    api = TqApi()
    kd = DataDownloader(api, symbol_list=SYMBOL, dur_sec=interval,
                        start_dt=datetime(2019, 5, 15, 21, 0 ,0), end_dt=datetime(2019, 12, 21, 16, 0, 0), csv_file_name=filename)

    # 使用with closing机制确保下载完成后释放对应的资源
    with closing(api):
        while not kd.is_finished():
            api.wait_update()
            print("progress: kline: %.2f " % (kd.get_progress()))
