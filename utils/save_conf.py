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
    cf.set(section_name, "app_interference", data_path + "scheduling_preliminary_app_interference_20180606.csv")
    cf.set(section_name, "app_resources", data_path + "scheduling_preliminary_app_resources_20180606.csv")
    cf.set(section_name, "instance_deploy", data_path + "scheduling_preliminary_instance_deploy_20180606.csv")
    cf.set(section_name, "machine_resources", data_path + "scheduling_preliminary_machine_resources_20180606.csv")
    cf.set(section_name, "instance", data_path + "instance.csv")
    cf.set(section_name, "app", data_path + "app.csv")

    if not cf.has_section("table_size"):
        cf.add_section("table_size")
    cf.set("table_size", "app_size", "9338")
    cf.set("table_size", "machine_size", "6000")
    cf.set("table_size", "instance_size", "68219")
    cf.set("table_size", "app12_size", "35242")

    if not cf.has_section("system_config"):
        cf.add_section("system_config")
    cf.set("system_config", "debug", "true")

    if not cf.has_section("db_mysql"):
        cf.add_section("db_mysql")
    cf.set("db_mysql", "db_host", "localhost")
    cf.set("db_mysql", "db_port", "3306")
    cf.set("db_mysql", "db_user", "root")
    cf.set("db_mysql", "db_pass", "1233456")

    with open(config_file, "w") as f:
        cf.write(f)


def read():
    cf.read(config_file)
    print(cf.get(section_name, "app_interference"))
