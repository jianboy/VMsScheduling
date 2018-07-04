#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 15:55
@File :main.py
'''
from configparser import ConfigParser

config_file = "../conf/config.ini"
data_path = "../data/"
section_name = "data_file_name"
cf = ConfigParser()


def write():
    if not cf.has_section(section_name):
        cf.add_section(section_name)
    cf.set(section_name, "app_interference", data_path+"scheduling_preliminary_app_interference_20180606.csv")
    cf.set(section_name, "app_resources", data_path+"scheduling_preliminary_app_resources_20180606.csv")
    cf.set(section_name, "instance_deploy", data_path+"duling_preliminary_instance_deploy_20180606.csv")
    cf.set(section_name, "machine_resources", data_path+"scheduling_preliminary_machine_resources_20180606.csv")
    with open(config_file, "w") as f:
        cf.write(f)


def read():
    cf.read(config_file)
    print(cf.get(section_name, "app_interference"))

write()