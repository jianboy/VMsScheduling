#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
测试数据准备，instance.py总共68219条数据，只取628条数据。
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/9 8:12
@File :test_data.py
'''
import pandas as pd


def prepareInstance():
    df3 = pd.read_csv("../data/instance.csv")
    df3 = df3.iloc[0:628, :]
    df3.to_csv("../data/test-instance.csv")
    print(df3.shape)

def perpare():
    pass

# prepareInstance()