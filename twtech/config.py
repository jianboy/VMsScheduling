#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/7 3:04
@File :config.py
'''
from configparser import ConfigParser

cf = ConfigParser()
config_path = "../conf/config.ini"
section_name = "data_file_name"
cf.read(config_path)


class Config():
    def __init__(self):
        pass

    def getConfig(self):
        return self

    def setConfig(self, db_mysql, sysconfig, file):
        pass

    def setConfigByDB(self, db_mysql):
        self.db_mysql = ""