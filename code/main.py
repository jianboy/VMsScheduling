#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 15:55
@File :main.py
'''

# 数据预览
import pandas as pd
from configparser import ConfigParser

import libs.save_conf

class Scheduling():
    sb=[]
    df3=None
    
    def init(self,name,gender,birth,**kw):
        self.name = name
        self.gender = gender
        self.birth = birth
        for k,v in kw.iteritems() :
            setattr(self,k,v)
        self.import_data()

    def import_data():
        df3=pd.read_csv("app")

# step1: 数据参数初始化
    def getConfig(self):
        cf = ConfigParser()
        config_path = "../conf/config.ini"
        section_name = "data_file_name"
        cf.read(config_path)

        app_interference = cf.get(section_name, "app_interference")
        app_resources = cf.get(section_name, "app_resources")
        instance_deploy = cf.get(section_name, "instance_deploy")
        machine_resources = cf.get(section_name, "machine_resources")


    def init_conf(self):
        '''
        初始化配置文件
        :retur
        '''
        libs.save_conf.write()

    def sort_dynamic(self):


if __name__ == '__main__':
    init_conf()
