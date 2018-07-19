#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/8 2:57
@File :save_result.py
'''

import datetime

import pandas as pd


def save_result(df):
    '''
    导出数据结果
    :param data:
    :return:
    '''

    # head = ["instance", "machine"]
    # data = [["ss", "aa"], ["ss", "aa"], ["ss", "aa"], ["ss", "aa"]]

    # df = pd.DataFrame(data, columns=head)
    df.to_csv(("../submit/submit_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"), header=None,
              index=False)
