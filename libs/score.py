#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
得分计算
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/6 1:51
@File :score.py
'''
import math

# Sjt表示j主机在t时刻的得分score。

flag = True
alpha = 10
beta = 0.5

def getScore():
    '''
    计算得分
    :return:
    '''
    sum=0
    for j in range(0, 6000):
        for t in range(0,92):
            # c表示j主机在t时刻的CPU利用率
            c = (1 + 2 + 3) / 50
            if flag == False:
                Sjt = 0
            else:
                Sjt = 1 + alpha * (math.exp(max(0, c - beta)))
                sum=sum+Sjt
