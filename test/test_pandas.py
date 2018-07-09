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


def t6():
    df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "111", "B": "121"}, {"A": "1111", "B": "1211"}])

    print(df)
    print(df.columns.size)  # 列数 2
    h, l = df.shape
    print(h, l)
    print(df.iloc[:, 0].size)  # 行数 3
    print(df.ix[[0]].index.values[0])  # 索引值 0
    print(df.ix[[0]].values[0][0])  # 第一行第一列的值 11
    print(df.ix[[1]].values[0][1])  # 第二行第二列的值 121


def t7():
    '''
    增加一行/一列
    :return:
    '''
    df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "1111", "B": "1211"}])
    # df.insert(value=list([22, 33]))
    df = df.append(pd.DataFrame([{"A": "1133", "B": "1332"}]))
    print(df)

    # 增加一列：
    df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "1111", "B": "1211"}])
    df["is"] = False
    print(df)


def t8():
    # 修改值不能直接引用：df3["mem"][i]，而需要df3.loc["mem"][i]
    df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "1111", "B": "1211"}])
    df["is"] = False
    # df["is"][0] = True
    # df.loc[0][2] = True
    # df.loc[:, "is"] = True
    df.loc[0, "is"] = True
    print(df)


# DataFrame循环遍历
def t9():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 4, 5]})
    for row in df.itertuples():
        print("the index", row.Index)
    print("sum of row", row.a + row.b)


t9()

# result = pd.DataFrame(columns=list(["instanceid", "machineid"]), data=list())

# df = pd.DataFrame({'a': list(range(100)), 'b': [random.random() for i in range(100)]})
# index = pd.MultiIndex.from_product([list('abcd'), list(range(25))])
# df.index = index
# print(df.head())
# df.loc[('a', -1), :] = None
# df.tail()
#
# data = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
# data.index = pd.MultiIndex.from_tuples([('a', 1), ('b', 1), ('c', 1)])
# data
# new_df = df.append(data)
# new_df.tail()
