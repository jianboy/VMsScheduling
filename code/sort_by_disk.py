#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
按照磁盘占用率从大到小装箱，即按照磁盘先用完为止进行分配实例到主机。
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 0:43
@File :sort_by_disk.py
'''

import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
from configparser import ConfigParser
import time
import libs.save_result

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)

app_interference = cf.get(section_name, "app_interference")
app_resources = cf.get(section_name, "app_resources")
instance_deploy = cf.get(section_name, "instance_deploy")
machine_resources = cf.get(section_name, "machine_resources")
app = cf.get(section_name, "app")
instance = cf.get(section_name, "instance")
# app
df1 = pd.read_csv(app_resources, encoding="utf-8")

# instance
df3 = pd.read_csv(instance_deploy, header=None,
                  names=list(["instanceid", "appid", "machineid"]))

# machine
# 其实就两类，所以就不需要导入数据了。

# 限制表
df4 = pd.read_csv(app_interference, header=None,
                  names=list(["appid1", "appid2", "max_interference"]), encoding="utf-8")

result = pd.DataFrame(columns=list(["instanceid"], "machineid"))

tem_disk = tem_mem = tem_cpu = tem_P = tem_M = tem_PM = 0
tmp_stand_cpu1 = 32
tmp_stand_mem1 = 64
tmp_stand_disk1 = 600

tmp_stand_cpu2 = 92
tmp_stand_mem2 = 288
tmp_stand_disk2 = 600

tmp_stand_P = 7
tmp_stand_M1 = 3
tmp_stand_M2 = 7
tmp_stand_PM1 = 7
tmp_stand_PM2 = 9

machine_count = 0  # 3000小机器，3000大机器。所以在小机器用完换大机器
j = 1  # j表示主机序号，从1-3000，3001到6000
is_deploy = False  # 主机j是否部署了instance
deploy_list = list()  # 主机j部署的instanceid实例


# 各app之间的限制
def restrictApp(instance, deploy_list):
    # df4["appid1"]
    # df4["appid2"]

    return True


# 执行部署方案
def deplay():
    print("------------开始部署啦--------------")
    start = time.time()
    row, column = df3.shape
    while row > 0:
        deployInstance(row, j)
        # 整个instace都遍历了，第j主机无法再放入一个，所以添加j+1主机
        row, column = df3.shape
        j = j + 1

    # 部署完事
    print("------------部署完啦--------------")
    end = time.time()
    print("总共耗时：", end - start, "秒")
    print("总共需要主机数：", j)
    print("部署方案前几条示意：", result.head())
    libs.save_result.save_result(result)


def deployInstance(mlength, j):
    '''
    根据限制部署实例到主机上
    :param mlength: 根据剩余的instance数量循环
    :param j: 第j台主机
    :return: 暂未定返回值，None
    '''
    global is_deploy, tem_disk, tem_mem, tem_cpu, tem_P, tem_M, tem_PM
    for i in range(0, mlength):
        tem_disk = tem_disk + df3["disk"][i]  # 当前磁盘消耗
        tem_mem = tem_mem + df3["mem"][i]
        tem_cpu = tem_cpu + df3["cpu"][i]
        tem_P = tem_P + df3["P"][i]
        tem_M = tem_M + df3["M"][i]
        tem_PM = tem_PM + df3["PM"][i]

        # if 满足限制表条件，则把当前实例部署到这台主机上。
        if is_deploy == True:
            if tem_disk < tmp_stand_disk1:  # 磁盘够
                if restrictApp(instance=df3["instanceid"], deploy_list=deploy_list):
                    if tem_mem < tmp_stand_mem1:  # 内存够
                        if tem_cpu < tmp_stand_cpu1:  # CPU够
                            if tem_M < tmp_stand_M1:
                                if tem_P < tmp_stand_P:
                                    if tem_PM < tmp_stand_PM1:
                                        result["machine"][i] = "machine_" + i
        else:
            # 主机j没有部署实例，则先部署一个
            result["machine"][i] = "machine_" + i
            is_deploy = True
    is_deploy = False


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
