#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 15:55
@File :main.py
'''

# 数据预览
from configparser import ConfigParser

import libs.save_conf


# step1: 数据参数初始化
def getConfig():
    cf = ConfigParser()
    config_path = "../conf/config.ini"
    section_name = "data_file_name"
    cf.read(config_path)

    app_interference = cf.get(section_name, "app_interference")
    app_resources = cf.get(section_name, "app_resources")
    instance_deploy = cf.get(section_name, "instance_deploy")
    machine_resources = cf.get(section_name, "machine_resources")


def init_conf():
    '''
    初始化配置文件
    :return:
    '''
    libs.save_conf.write()


if __name__ == '__main__':
    init_conf()
