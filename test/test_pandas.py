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
    '''
    切片：
    :return:
    '''
    df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "111", "B": "121"}, {"A": "1111", "B": "1211"}])

    print(df)
    print(df.columns.size)  # 列数 2
    h, l = df.shape
    print(h, l)  # 3,2
    print(df.iloc[:, 0].size)  # 行数 3
    print(df.ix[[0]].index.values[0])  # 索引值 0
    print(df.ix[[0]].values[0][0])  # 第一行第一列的值 11
    print(df.ix[[1]].values[0][1])  # 第二行第二列的值 121
    print(df.A, df.B)
    print(df["A"], df["B"])
    print(df.loc["A"])
    print(df.loc[df["A"] > 1])
    print(df.loc[pd.isna(df["A"])] == False)
    print(df[df.isna["A"]] == False)  # .loc可以省略
    # iloc和loc：iloc按0，1，2，3等索引每行；loc按每列的列名索引


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
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 4, "C"]})
    for row in df.itertuples():
        print(row.a, row.b)

    for row in df.items():
        print(row[1][0], row[1][1], row[1][2])

    # 不推荐
    for row in df.iteritems():
        print(row[1][0], row[1][1], row[1][2])

    # 不推荐
    for row in df:
        print(df[row][0], df[row][1], df[row][2])


def t10():
    for i in range(10):
        print(i)


def t11():
    '''

    :return:
    '''
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 4, "C"]})
    print(df)
    df1 = df
    df2 = df.copy()  # 正确
    df1.a = [2, 2, 2]  # 直接使用=只传址，df,df1任何更改，两个变量都更改
    df.b = [3, 3, 3]
    print(df1)


def t12():
    '''
    字符分割1 appid原来字符表示，现在去掉app_，直接用后缀数字表示。
    '''
    df = pd.DataFrame({'appid': ["app_1", "app_2", "app_3"], 'cpu': [3, 4, "C"]},
                      columns=list(["appid", "cpu"]))
    # tmp = pd.to_numeric(df["appid"].str.split("_", expand=True)[1].values)
    # df[['col2', 'col3']] = df[['col2', 'col3']].apply(pd.to_numeric)
    df["appid"] = pd.to_numeric(df["appid"].str.split("_", expand=True)[1].values)
    print(df)


def t13():
    '''
    字符串分割2
    :return:
    '''
    s = pd.DataFrame(['a,b,c', 'c,d,e'])
    print(s)

    temp_expend_False = s[0].str.split(',')
    print(temp_expend_False)

    temp_expend_True = s[0].str.split(',', expand=True)
    print(temp_expend_True)
    print(temp_expend_True[1].values)


t12()

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
