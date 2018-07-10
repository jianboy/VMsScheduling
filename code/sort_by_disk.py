#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按照磁盘占用率从大到小装箱，即按照磁盘先用完为止进行分配实例到主机。
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 0:43
@File :sort_by_disk.py
"""

import matplotlib

matplotlib.use('Agg')

import pandas as pd
from configparser import ConfigParser
import time
import libs.save_result

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)

app_interference = cf.get(section_name, "app_interference")
app_resources = cf.get(section_name, "app_resources")
instance = cf.get(section_name, "instance")
# app
df1 = pd.read_csv(app_resources, encoding="utf-8")

# instance
df3 = pd.read_csv(instance)
# df3 = pd.read_csv("../data/test-instance.csv")

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
tmp_stand_disk2 = 1024

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
def restrict_apps(instance, deploy_list):
    len_list = len(deploy_list)
    if len_list == 0:
        return True
    else:
        ct = pd.Series(deploy_list).value_counts()
        for k, v in ct.items():
            # tmp表示在df4中找到限制条件一行
            tmp = df4.loc[(df4["appid1"] == k) & (df4["appid2"] == instance)]
            row, col = tmp.shape
            if row > 0:
                if instance in ct.index:
                    if k == instance:
                        # a a 2 表示有一个a前提，还可以放2个a，最多可以放3个a
                        if ct[instance] > tmp["max_interference"].values[0]:
                            return False
                    else:
                        # a b 2 表示有一个a前提，还可以放2个b，最多可以放2个b
                        if ct[instance] + 1 > tmp["max_interference"].values[0]:
                            return False
                else:
                    # a e 2 表示有一个a前提，还可以放2个e，最多可以放2个b ct[instance]=0
                    if 1 > tmp["max_interference"].values[0]:
                        return False
        return True


# 执行部署方案
def deploy():
    global j, is_deploy, tem_mem, tem_cpu, tem_disk, tem_P, tem_M, tem_PM, tem_pre_disk, tem_pre_mem, \
        tem_pre_cpu, tem_pre_P, tem_pre_M, tem_pre_PM, result, df3, deploy_list

    print("------------开始部署啦--------------")
    start = time.time()
    row, column = df3.shape
    while row > 0:
        deployInstance()
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
        print("已经部署：", 68219 - row, "剩余部署Instance数据：", row)
        print("已经消耗Machine主机数据：", j)
        print("已经消耗时间：", time.time() - start, "秒")

    # 部署完事
    print("------------部署完啦--------------")
    end = time.time()
    print("总共耗时：", end - start, "秒")
    print("总共需要主机数：", j)
    print("部署方案前几条示意：", result.head())
    libs.save_result.save_result(result)


def deployInstance():
    """
    根据限制部署实例到主机上
    :return: 暂未定返回值，None
    """
    global is_deploy, tem_mem, tem_cpu, tem_disk, tem_P, tem_M, tem_PM, tem_pre_disk, \
        tem_pre_mem, tem_pre_cpu, tem_pre_P, tem_pre_M, tem_pre_PM, result, j, df3, deploy_list
    for row in df3.itertuples():
        i = row.Index
        tem_pre_cpu = tem_cpu + row.cpu
        tem_pre_mem = tem_mem + row.mem
        tem_pre_disk = tem_disk + row.disk  # 当前磁盘消耗
        tem_pre_P = tem_P + row.P
        tem_pre_M = tem_M + row.M
        tem_pre_PM = tem_PM + row.PM

        # if 满足限制表条件，则把当前实例部署到这台主机上。
        if j > 3000:  # 使用小主机
            if is_deploy:
                if tem_pre_disk <= tmp_stand_disk1:  # 磁盘够
                    if restrict_apps(instance=row.instanceid, deploy_list=deploy_list):
                        if tem_pre_mem < tmp_stand_mem1:  # 内存够
                            if tem_pre_cpu < tmp_stand_cpu1:  # CPU够
                                if tem_pre_M <= tmp_stand_M1:
                                    if tem_pre_P <= tmp_stand_P:
                                        if tem_pre_PM <= tmp_stand_PM1:
                                            # 条件都满足，则把instance放入主机，同时df3表中去掉这个部署好的一行
                                            result = result.append(pd.DataFrame(
                                                [{"instanceid": row.instanceid,
                                                  "machineid": "machine_" + str(j)}]))
                                            tem_disk = tem_disk + row.disk
                                            tem_mem = tem_mem + row.mem
                                            tem_cpu = tem_cpu + row.cpu
                                            tem_P = tem_P + row.P
                                            tem_M = tem_M + row.M
                                            tem_PM = tem_PM + row.PM
                                            df3.loc[i, "isdeploy"] = True
                                            deploy_list.append(row.instanceid)

            else:
                # 主机j没有部署实例，则先部署一个
                result = result.append(
                    pd.DataFrame([{"instanceid": row.instanceid, "machineid": "machine_" + str(j)}]))
                tem_disk = tem_disk + row.disk
                tem_mem = tem_mem + row.mem
                tem_cpu = tem_cpu + row.cpu
                tem_P = tem_P + row.P
                tem_M = tem_M + row.M
                tem_PM = tem_PM + row.PM
                df3.loc[i, "isdeploy"] = True
                deploy_list.append(row.instanceid)
                # df3["isdeploy"][i] = True
                is_deploy = True
        else:  # 使用大主机
            if is_deploy:
                if tem_pre_disk <= tmp_stand_disk2:  # 磁盘够
                    if restrict_apps(instance=row.instanceid, deploy_list=deploy_list):
                        if tem_pre_mem < tmp_stand_mem2:  # 内存够
                            if tem_pre_cpu < tmp_stand_cpu2:  # CPU够
                                if tem_pre_M <= tmp_stand_M2:
                                    if tem_pre_P <= tmp_stand_P:
                                        if tem_pre_PM <= tmp_stand_PM2:
                                            # 条件都满足，则把instance放入主机
                                            result = result.append(pd.DataFrame(
                                                [{"instanceid": row.instanceid,
                                                  "machineid": "machine_" + str(j)}]))
                                            tem_disk = tem_disk + row.disk
                                            tem_mem = tem_mem + row.mem
                                            tem_cpu = tem_cpu + row.cpu
                                            tem_P = tem_P + row.P
                                            tem_M = tem_M + row.M
                                            tem_PM = tem_PM + row.PM
                                            df3.loc[i, "isdeploy"] = True
                                            deploy_list.append(row.instanceid)

            else:
                # 主机j没有部署实例，则先部署一个
                result = result.append(
                    pd.DataFrame([{"instanceid": row.instanceid, "machineid": "machine_" + str(j)}]))
                tem_disk = tem_disk + row.disk
                tem_mem = tem_mem + row.mem
                tem_cpu = tem_cpu + row.cpu
                tem_P = tem_P + row.P
                tem_M = tem_M + row.M
                tem_PM = tem_PM + row.PM
                df3.loc[i, "isdeploy"] = True
                deploy_list.append(row.instanceid)
                is_deploy = True


deploy()
