#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/5 0:56
@File :data_preview.py
'''

# 后台做图，不需要GUI需要在头部第一行加入下面两行代码
# %matplotlib inline   jupyter中加入这一行
import matplotlib
matplotlib.use('Agg')

# 数据预览
import pandas as pd
import matplotlib.pyplot as plt
from configparser import ConfigParser

# step1: 数据参数初始化

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)

app_interference = cf.get(section_name, "app_interference")
app_resources = cf.get(section_name, "app_resources")
instance_deploy = cf.get(section_name, "instance_deploy")
machine_resources = cf.get(section_name, "machine_resources")

def for_df1():
    # 应用app表: 应用id/cpu占用量/内存占用/磁盘占用/P/M/PM等指标
    df1 = pd.read_csv(app_resources, header=None,
                      names=list(["appid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
    print(df1.dtypes)
    # appid    object
    # cpu      object
    # mem      object
    # disk      int64
    # P         int64
    # M         int64
    # PM        int64
    print(df1.shape)
    # (9338, 7)
    # [5 rows x 7 columns]
    # print(df1.head())
    # app_3 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0....... 0 0
    tmp = df1["cpu"].str.split('|', expand=True).astype('float')
    # [5 rows x 98 columns]
    df1["cpu"] = tmp.T.mean().T  # 转置,求均值，再转置回来，这样求得一行的均值。

    tmp = df1["mem"].str.split('|', expand=True).astype('float')
    # [5 rows x 98 columns]
    df1["mem"] = tmp.T.mean().T  # 转置,求均值，再转置回来，这样求得一行的均值。
    print(df1.head())
    print("总共应用：", df1["appid"].unique().shape)


def for_df2():
    # 主机表 ：宿主机id/ cpu规格/mem规格/disk规格/P上限/M上限/PM上限
    df2 = pd.read_csv(machine_resources, header=None, names=list(
        ["machineid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
    # df2 = pd.DataFrame(pd.read_csv("../data/scheduling_preliminary_machine_resources_20180606.csv", header=None),columns=list(["machineid", "cpu", "mem", "disk", "P", "M", "PM"]))
    print(df2.dtypes)
    # machineid    object
    # cpu      int
    # mem      int
    # disk      int64
    # P         int64
    # M         int64
    # PM        int64
    print(df2.shape)
    # (6000, 7)
    print(df2.head())
    # machine_3   32   64   600  7  3   7
    print("总共主机：", df2["machineid"].unique().shape)
    # 6000

    # 这里主机主要就两类：
    # machine_1	32	64	600  	7	3	7    数量：3000
    # machine_2	92	288	1024	7	7	9   数量：3000


def for_df3():
    # 主机machine/实例instance/应用app 关系表
    df3 = pd.read_csv(instance_deploy, header=None,
                      names=list(["instanceid", "appid", "machineid"]), encoding="utf-8")
    print(df3.dtypes)
    print("df数据大小：", df3.shape)
    print("instance唯一数量：", df3["instanceid"].unique().shape)
    # print(df2["instanceid"])
    print("总共实例：", df3["instanceid"].unique().shape)


def for_df4():
    # 主机和实例表。部署appid1的insterference最多可以部署n个appid2
    df4 = pd.read_csv(app_interference, header=None,
                     names=list(["appid1", "appid2", "max_interference"]), encoding="utf-8")
    # 查看数据类型
    # print(df.dtypes)
    print("df数据大小：", df4.shape)

    # 查看头尾部数据
    # app_8361  app_2163  0
    # app_6585  app_8959  0
    # print(df.head())
    # print(df.tail())

    # 查看索引
    # print(df.index)
    # 查看所有列标
    # print(df.columns)
    # 查看所有数据
    # print(df.values)

    # 第一列
    # df[0].groupby()

    # 第二列

    # 第三列

    # 描述性统计
    print("数据预览：", df4.describe())

    plt.plot(df4["max_interference"])
    plt.savefig("../submit/fig1.png")


for_df4()
