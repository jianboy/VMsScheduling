#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/6 16:59
@File :plot.py
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # 导入模块

squares = [1, 4, 9, 16, 25]  # 指定列表Y坐标为列表中的值，X坐标为列表下标
plt.plot(squares)  # 传入列表
plt.show()
plt.savefig("../submit/t1.jpg")