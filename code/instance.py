#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
按照app对instance分类,存储一个新的instance.csv文件，后面添加了cpu,mem，disk,P,M,PM等几列
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/6 16:13
@File :instance.py
'''

from configparser import ConfigParser

import pandas as pd

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)

app_interference = cf.get(section_name, "app_interference")
app = cf.get(section_name, "app")
instance_deploy = cf.get(section_name, "instance_deploy")
machine_resources = cf.get(section_name, "machine_resources")

# app
df1 = pd.read_csv(app, encoding="utf-8")

# instance
df3 = pd.read_csv(instance_deploy, header=None,
                  names=list(["instanceid", "appid", "machineid"]))

# instance分类统计
group1 = df3.groupby("appid").count()
print(type(group1))
# print(group1["instanceid"].sort_values(ascending=False))
# plt.plot(group1["instanceid"].sort_values(ascending=False))
# plt.savefig("../submit/group1.jpg")

# 找到每个instance消耗的disk
df3["cpu"] = None
df3["disk"] = None
df3["mem"] = None
df3["P"] = None
df3["M"] = None
df3["PM"] = None

for i in range(0, int(cf.get("table_size", "instance_size"))):
    # df1[df1["appid"] == df3["appid"][i]]["disk"]返回一个pd.Series对象（列表），其实只有一个值，需要选定第一个即可
    df3["mem"][i] = df1[df1["appid"] == df3["appid"][i]]["mem_avg"].values[0]
    df3["cpu"][i] = df1[df1["appid"] == df3["appid"][i]]["cpu_avg"].values[0]
    df3["disk"][i] = df1[df1["appid"] == df3["appid"][i]]["disk"].values[0]
    df3["P"][i] = df1[df1["appid"] == df3["appid"][i]]["P"].values[0]
    df3["M"][i] = df1[df1["appid"] == df3["appid"][i]]["M"].values[0]
    df3["PM"][i] = df1[df1["appid"] == df3["appid"][i]]["PM"].values[0]

# ascending=False 降序
df3 = df3.sort_values(ascending=False, by="disk")

df3.to_csv("../data/instance.csv")
