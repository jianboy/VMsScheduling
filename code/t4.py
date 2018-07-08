#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/8 22:15
@File :t4.py
'''
import pandas as pd

df = pd.DataFrame([{"A": "11", "B": "12"}, {"A": "1111", "B": "1211"}])
df["isdploy"] = False
df.loc[0, "isdploy"] = True

df = df[df["isdploy"] == False]



# df["is"][0] = True
# df.loc[0][2] = True
# df.loc[:, "is"] = True
# df.set_value(index="0", col="isdploy", value=False)
# print(df.get_value(index="isdploy", col=0))
print(df)
