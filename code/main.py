#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 15:55
@File :main.py
'''
import os,sys
import numpy as np,pandas as pd
import matplotlib.pyplot as plt

#Wij矩阵表示第i个instance实例部署到j主机上
Wij_size = np.zeros((68219, 6000))
Wij = np.zeros_like(Wij_size)

def getWij():
    # inst_26195, app_147, machine_1149
    df3=pd.read_csv("../data/scheduling_preliminary_instance_deploy_20180606.csv", header=None,names=list(["instanceid", "appid", "machineid"]))
    for i in range(0,68219):
            if df3[i]["machineid"]==None:
                pass
            else:
                # Wij[i][j]=
                pass

def import_data():
    pass

if __name__ == '__main__':
    getWij()

