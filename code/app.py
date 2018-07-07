#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
对app表处理，计算平均CPU，mem，在app表添加两列保存其值
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 3:14
@File :app.py
'''

import matplotlib

matplotlib.use('Agg')

# 数据预览
import pandas as pd
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

# app表
df1 = pd.read_csv(app_resources, header=None,
                  names=list(["appid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")

# 新添加两列
df1["cpu_avg"] = None
df1["mem_avg"] = None

# expand=True表示
tmp = df1["cpu"].str.split('|', expand=True).astype('float')
# [9338 rows x 98 columns]
df1["cpu_avg"] = tmp.T.mean().T  # 转置,求均值，再转置回来，这样求得一行的均值。

tmp = df1["mem"].str.split('|', expand=True).astype('float')
df1["mem_avg"] = tmp.T.mean().T  # 转置,求均值，再转置回来，这样求得一行的均值。
print(df1.head())
print("总共应用：", df1["appid"].unique().shape)

df1.pop("cpu")
df1.pop("mem")
df1.to_csv("../data/app.csv")
