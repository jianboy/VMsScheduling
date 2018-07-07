#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/5 3:08
@File :test_pandas.py
'''
import pandas as pd

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
    df = pd.DataFrame()
    df2 = pd.read_csv()
    df3 = pd.Series()
    pd.concat()
    pd.to_datetime()
    pd.merge()
    pd.Timestamp


def t4():
    df = pd.DataFrame(columns=list("AB"), data=[[1, 2], [3, 4]])
    df["C"] = None
    df["C"][1] = 2
    print(df)


def t5():
    ser1 = pd.Series([1, 2, 3, 4])
    ser2 = pd.Series(range(4), index=["a", "b", "c", "d"])
    sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
    ser3 = pd.Series(sdata)
    # print(ser1)
    print(ser2)

    # 访问Series
    ser2["a"]
    # 所有索引
    ser2.index
    # 所有值
    ser2.values


t5()
