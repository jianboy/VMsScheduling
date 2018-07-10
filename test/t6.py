#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/10 20:36
@File :t6.py
'''
import datetime

import pandas as pd

df3 = pd.read_csv("../submit/submit_20180710_164012.csv", names=list(["instanceid", "machineid"]))
df3["machineid"] = df3["machineid"].sort_index(ascending=False).values
df3.to_csv(("../submit/submit_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"), header=None,
           index=False)
# print(df3)
