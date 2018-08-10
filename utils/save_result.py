#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/8 2:57
@File :save_result.py
'''

import datetime.datetime
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
    df.to_csv(("../submit/submit_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"), header=None,
              index=False)


def marge_ab(df_a, df_b):
    '''
    合并数据，并导出
    :param df_a:
    :param df_b:
    :return:
    '''
    path_ab = "submit_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"
    df_ab = pd.merge(df_a, df_b)

    df_ab.to_csv(path_ab, header=None, index=False)
