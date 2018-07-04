#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 16:46
@File :read_file.py
'''

import csv
from configparser import ConfigParser

config_path = "../conf/config.ini"
section_name = "data_file_name"
cf = ConfigParser()
cf.read(config_path)
# app_interference
# app_resources
# instance_deploy
# machine_resources

with csv.reader(cf.get(section_name, "app_interference"), "r") as f:
    for line in f:
        print(line)
