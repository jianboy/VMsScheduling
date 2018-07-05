#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/5 3:08
@File :test_pandas.py
'''
import pandas as pd ,numpy as np


def t1():
    a = [['a', '1.2', '4.2'], ['b', '70', '0.03'], ['x', '5', '0']]
    df = pd.DataFrame(a, columns=list("ABC"))
    print(df.dtypes)
    print(df)

def t2():
    obj = pd.Series(list('cadaabbcc'))
    uniques = obj.unique()
    print(obj.dtypes)
    print(uniques.shape)

def t3():
    df=pd.DataFrame()
    df2=pd.read_csv()
    df3=pd.Series()
    pd.concat()
    pd.to_datetime()
    pd.merge()
    pd.Timestamp


t2()