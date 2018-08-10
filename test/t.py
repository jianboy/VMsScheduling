# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/8 3:16
@File :t.py
'''
import pandas as pd


def t1():
    # list
    cpuIter = list()
    for i in range(10):
        cpuIter.append(i)
    print(cpuIter)


def t2():
    # dict
    res = list()
    n = 5
    for i in range(n):
        res.append({})
    res[1] = {"A": 2, "B": 3}
    res.append({"appid": 0})
    print(res[1].get("C") == None)
    print(res)


def t3():
    # pandas dataframe
    result = pd.DataFrame(columns=list(["instanceid", "machineid"]), data=list())
    for i in range(5):
        # result = result.append(pd.DataFrame(
        #     [{"instanceid": "2",
        #       "machineid": "machine_" + str(2)}]))
        result = result.append(
            [{"instanceid": "2",
              "machineid": "machine_" + str(2)}])
    print(result)


t2()
