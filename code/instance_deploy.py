#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 3:58
@File :instance_deploy.py
'''
# 数据预览
from configparser import ConfigParser

import pandas as  pd

# step1: 数据参数初始化

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)

app_interference = cf.get(section_name, "app_interference")
app_resources = cf.get(section_name, "app_resources")
instance_deploy = cf.get(section_name, "instance_deploy")
machine_resources = cf.get(section_name, "machine_resources")

df3 = pd.read_csv(instance_deploy, header=None,
                  names=list(["instanceid", "appid", "machineid"]), encoding="utf-8")

# print(df3[df3["machineid"] == "NaN"])
# print(df3.head())

print(pd.isna(df3["machineid"]).value_counts())
# True     38223
# False    29996 还有一半没有部署