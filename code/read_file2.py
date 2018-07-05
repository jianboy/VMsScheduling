#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
使用pandas 读取数据
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 17:15
@File :read_file2.py
'''

from  configparser import ConfigParser

import pandas as pd

config_path = "../conf/config.ini"
section_name = "data_file_name"
cf = ConfigParser()
cf.read(config_path)
# app_interference
# app_resources
# instance_deploy
# machine_resources

df = pd.read_csv(cf.get(section_name, "app_interference"), encoding="utf-8")
print("数据类型：", df.dtypes)
print("数据大小：", df.shape)
