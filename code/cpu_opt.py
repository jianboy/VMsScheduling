#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/9 7:54
@File :cpu_opt.py
'''
import pandas as pd


def getWij():
    global machine_resources
    # Wij矩阵表示第i个instance实例部署到j主机上
    Wij_size = np.zeros((68219, 6000))
    Wij = np.zeros_like(Wij_size)

    # inst_26195, app_147, machine_1149
    df3=pd.read_csv("../data/instance.csv", header=None,names=list(["instanceid", "appid", "machineid","disk"]))
    df2 = pd.read_csv(machine_resources, header=None, names=list(
        ["machineid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
    for i in range(0,68219):
            if df3[i]["machineid"]==None:
                pass
            else:
                # Wij[i][j]=
                pass
