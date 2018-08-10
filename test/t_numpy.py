#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
注意文件名不要和Numpy等导入的包一样，否则导入包出错！
@Auther :liuyuqi.gov@msn.cn
@Time :7/20/2018 7:00 AM
@File :t_numpy.py
'''

import numpy as np

x = np.array([[1, 2, 3], [9, 8, 7], [6, 5, 4]])


def t1():
    '''
    定义ndarray数组
    :return:
    '''
    x = np.array([[1, 2, 3], [9, 8, 7], [6, 5, 4]])
    print(x)
    print(x.shape)  # 行，列数
    print(type(x))  # 类型
    print(x.flags)  # 返回数组内部的信息
    print(x.size)  # 元素个数
    print(x.ndim)  # 维数


def t2():
    '''
    操作
    :return:
    '''
    # 转置
    print(x.T)

    # 切片
    # 将数组变为1维数组，并获取其中的一部分数据
    print(x.flat[2:6])


def t3():
    '''
    计算，求和/均值
    :return:
    '''


def t4():
    '''
     1e-9 科学计数法，java中类似，10^(-9)
    :return:
    '''
    print(0.000001 < 1e-9)


t4()
