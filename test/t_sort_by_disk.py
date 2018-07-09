#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
由于数据很大，测试使用部分数据！
按照磁盘占用率从大到小装箱，即按照磁盘先用完为止进行分配实例到主机。
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 0:43
@File :sort_by_disk.py
'''

import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import time
import libs.save_result

df1 = pd.read_csv("../data/scheduling_preliminary_app_resources_20180606 - 副本.csv", encoding="utf-8")
df3 = pd.read_csv("../data/test-instance.csv")

# print(df3["cpu"].value_counts())
# print(df3.head())
df3["cpu"] = df3["cpu"].astype("float")
df3["disk"] = df3["disk"].astype("float")
df3["mem"] = df3["mem"].astype("float")
df3["M"] = df3["M"].astype("float")
df3["P"] = df3["P"].astype("float")
df3["PM"] = df3["PM"].astype("float")

df3["isdeploy"] = False
# machine
# 其实就两类，所以就不需要导入数据了。

# 限制表
df4 = pd.read_csv(app_interference, header=None,
                  names=list(["appid1", "appid2", "max_interference"]), encoding="utf-8")

result = pd.DataFrame(columns=list(["instanceid", "machineid"]), data=list())

tem_pre_disk = tem_pre_mem = tem_pre_cpu = tem_pre_P = tem_pre_M = tem_pre_PM = 0
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
def restrictApps(instance, deploy_list):
    len_list = len(deploy_list)
    if len_list == 0:
        return True
    else:
        ct = pd.Series(deploy_list).value_counts()
        for k, v in ct.items():
            tmp = df4.loc[(df4["appid1"] == k) & (df4["appid2"] == instance)]
            row, col = tmp.shape
            if row > 0:
                if ct[instance] + 1 > tmp["max_interference"]:
                    return False
            else:
                # 在限制表中找不到限制条件
                return True


# 执行部署方案
def deploy():
    global j, is_deploy, tem_mem, tem_cpu, tem_disk, tem_P, tem_M, tem_PM, tem_pre_disk, tem_pre_mem, \
        tem_pre_cpu, tem_pre_P, tem_pre_M, tem_pre_PM, result, df3, deploy_list

    print("------------开始部署啦--------------")
    start = time.time()
    row, column = df3.shape
    while row > 0:
        deployInstance(row)
        # 整个instace都遍历了，第j主机无法再放入一个，所以添加j+1主机
        df3 = df3[df3["isdeploy"] == False]
        row, column = df3.shape
        df3 = df3.reset_index(drop=True)
        j = j + 1
        # j++之后表示新建主机，所以新主机没有部署任何实例，为false，然后初始化所有其他参数
        is_deploy = False
        tem_pre_disk = tem_pre_mem = tem_pre_cpu = tem_pre_P = tem_pre_M = tem_pre_PM = 0
        tem_disk = tem_mem = tem_cpu = tem_P = tem_M = tem_PM = 0
        deploy_list = list()

    # 部署完事
    print("------------部署完啦--------------")
    end = time.time()
    print("总共耗时：", end - start, "秒")
    print("总共需要主机数：", j)
    print("部署方案前几条示意：", result.head())
    libs.save_result.save_result(result)


def deployInstance(row):
    '''
    根据限制部署实例到主机上
    :param row: 根据剩余的instance数量循环
    :param j: 第j台主机
    :return: 暂未定返回值，None
    '''
    global is_deploy, tem_mem, tem_cpu, tem_disk, tem_P, tem_M, tem_PM, tem_pre_disk, tem_pre_mem, tem_pre_cpu, tem_pre_P, tem_pre_M, tem_pre_PM, result, j, df3, deploy_list
    for i in range(0, row):
        tem_pre_cpu = tem_cpu + df3["cpu"][i]
        tem_pre_mem = tem_mem + df3["mem"][i]
        tem_pre_disk = tem_disk + df3["disk"][i]  # 当前磁盘消耗
        tem_pre_P = tem_P + df3["P"][i]
        tem_pre_M = tem_M + df3["M"][i]
        tem_pre_PM = tem_PM + df3["PM"][i]

        # if 满足限制表条件，则把当前实例部署到这台主机上。
        if j < 3000:  # 使用小主机
            if is_deploy == True:
                if tem_pre_disk < tmp_stand_disk1:  # 磁盘够
                    if restrictApps(instance=df3["instanceid"][i], deploy_list=deploy_list):
                        if tem_pre_mem < tmp_stand_mem1:  # 内存够
                            if tem_pre_cpu < tmp_stand_cpu1:  # CPU够
                                if tem_pre_M < tmp_stand_M1:
                                    if tem_pre_P < tmp_stand_P:
                                        if tem_pre_PM < tmp_stand_PM1:
                                            # 条件都满足，则把instance放入主机，同时df3表中去掉这个部署好的一行
                                            result = result.append(pd.DataFrame(
                                                [{"instanceid": df3["instanceid"][i],
                                                  "machineid": "machine_" + str(j)}]))
                                            tem_disk = tem_disk + df3["disk"][i]
                                            tem_mem = tem_mem + df3["mem"][i]
                                            tem_cpu = tem_cpu + df3["cpu"][i]
                                            tem_P = tem_P + df3["P"][i]
                                            tem_M = tem_M + df3["M"][i]
                                            tem_PM = tem_PM + df3["PM"][i]
                                            df3.loc[i, "isdeploy"] = True
                                            deploy_list.append(df3["instanceid"][i])

            else:
                # 主机j没有部署实例，则先部署一个
                result = result.append(
                    pd.DataFrame([{"instanceid": df3["instanceid"][i], "machineid": "machine_" + str(j)}]))
                tem_disk = tem_disk + df3["disk"][i]
                tem_mem = tem_mem + df3["mem"][i]
                tem_cpu = tem_cpu + df3["cpu"][i]
                tem_P = tem_P + df3["P"][i]
                tem_M = tem_M + df3["M"][i]
                tem_PM = tem_PM + df3["PM"][i]
                df3.loc[i, "isdeploy"] = True
                deploy_list.append(df3["instanceid"][i])
                # df3["isdeploy"][i] = True
                is_deploy = True
        else:  # 使用大主机
            if is_deploy == True:
                if tem_pre_disk < tmp_stand_disk2:  # 磁盘够
                    if restrictApps(instance=df3["instanceid"][i], deploy_list=deploy_list):
                        if tem_pre_mem < tmp_stand_mem2:  # 内存够
                            if tem_pre_cpu < tmp_stand_cpu2:  # CPU够
                                if tem_pre_M < tmp_stand_M2:
                                    if tem_pre_P < tmp_stand_P:
                                        if tem_pre_PM < tmp_stand_PM2:
                                            # 条件都满足，则把instance放入主机
                                            result = result.append(pd.DataFrame(
                                                [{"instanceid": df3["instanceid"][i],
                                                  "machineid": "machine_" + str(j)}]))
                                            tem_disk = tem_disk + df3["disk"][i]
                                            tem_mem = tem_mem + df3["mem"][i]
                                            tem_cpu = tem_cpu + df3["cpu"][i]
                                            tem_P = tem_P + df3["P"][i]
                                            tem_M = tem_M + df3["M"][i]
                                            tem_PM = tem_PM + df3["PM"][i]
                                            df3.loc[i, "isdeploy"] = True
                                            deploy_list.append(df3["instanceid"][i])

            else:
                # 主机j没有部署实例，则先部署一个
                result = result.append(
                    pd.DataFrame([{"instanceid": df3["instanceid"][i], "machineid": "machine_" + str(j)}]))
                tem_disk = tem_disk + df3["disk"][i]
                tem_mem = tem_mem + df3["mem"][i]
                tem_cpu = tem_cpu + df3["cpu"][i]
                tem_P = tem_P + df3["P"][i]
                tem_M = tem_M + df3["M"][i]
                tem_PM = tem_PM + df3["PM"][i]
                df3.loc[i, "isdeploy"] = True
                deploy_list.append(df3["instanceid"][i])
                is_deploy = True


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


# 跑
deploy()
