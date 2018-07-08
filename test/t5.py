#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/9 2:07
@File :t5.py
'''

import pandas as pd

obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print(obj3)
obj4 = obj3.reset_index(drop=True)
print(obj4)
print(type(obj4))

