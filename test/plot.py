#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/9 22:26
@File :plot.py
'''


def plotGroup():  # df3新建一列
    df3["disk"] = None
    for i in range(0, 68219):
        df3["disk"][i] = lambda x: x[i], df1["disk"]

    # instance分类统计
    group1 = df3.groupby("appid").count()
    print(type(group1))
    print(group1["instanceid"].sort_values(ascending=False))
    plt.plot(group1["instanceid"].sort_values(ascending=False))
    plt.savefig("../submit/group1.jpg")

    # 找到每个instance消耗的disk

    # df3["disk"] =
