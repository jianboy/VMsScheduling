#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/4 15:55
@File :main.py
'''

import time
from configparser import ConfigParser

import pandas as pd

import libs.save_conf


class Scheduling():
    '''
    调度
    '''

    # 参数
    alpha = 10
    beta = 0.5
    T = 98
    EXEC_LIMIT = 100000

    # 静态数据 n:app数 N:inst数 m:machine数 k:资源种类
    n = N = m = 0
    k = 200
    cpuIter = list()
    appIndex = {}
    machineIndex = {}
    inst2AppIndex = {}
    appIndexference = {}

    apps = list()
    machines = list()
    appResources = list()
    machineResources = list()

    # 动态数据
    inst2Machine = {}
    machineResourcesUsed = list()
    machineHasApp = pd.DataFrame(columns=list(["instanceid", "machineid"]), data=list())

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def loadData(self):
        '''   n
               app_resources.csv
               m
               machine_resources.csv
               N
               instance_deploy.csv
               iterference_cnt
               app_interference.csv
            judge framework
        '''
        app_interference, app_resources, instance_deploy, machine_resources = self.getConfig()
        # 1.app_resources 9338*201
        self.appResources = pd.read_csv(app_resources, header=None,
                                        names=list(["appid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")

        tmp_cpu = self.appResources["cpu"].str.split('|', expand=True).astype('float')
        tmp_mem = self.appResources["mem"].str.split('|', expand=True).astype('float')

        for i in range(self.T):
            # 新添加98列CPU限制
            # self.appResources["cpu_" + str(i)] = None
            # self.appResources["mem_" + str(i)] = None
            # 赋值
            self.appResources["cpu_" + str(i)] = tmp_cpu[i]
            self.appResources["mem_" + str(i)] = tmp_mem[i]

        # 去掉cpu/men两列
        self.appResources.pop("cpu")
        self.appResources.pop("mem")
        self.n, col = self.appResources.shape  # 9338*201 201列：appid,cpu_1,cpu_2,...mem_1,men_2....,P,M,PM

        # 2.machine_resources 6000*201
        self.machineResources = pd.read_csv(machine_resources, header=None, names=list(
            ["machineid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")

        for i in range(self.T):
            self.machineResources["cpu_" + str(i)] = self.machineResources["cpu"]
            self.machineResources["mem_" + str(i)] = self.machineResources["mem"]
        self.machineResources.pop("cpu")
        self.machineResources.pop("mem")

        self.machineResourcesUsed = self.machineResources.copy()

        for i in range(200):
            self.machineResourcesUsed.iloc[:, i + 1] = 0

        # 3.instance_deploy
        self.inst2Machine = pd.read_csv(instance_deploy, header=None,
                                        names=list(["instanceid", "appid", "machineid"]), encoding="utf-8")
        # 增加一个字段标注是否部署
        self.inst2Machine["isdeploy"] = False
        # # 4.app_interference 冲突表
        self.appIndexference = pd.read_csv(app_interference, header=None,
                                           names=list(["appid1", "appid2", "max_interference"]), encoding="utf-8")

        # instance按照磁盘消耗排序
        self.n, col = self.appResources.shape
        self.N, col = self.machineResources.shape
        self.m, col = self.inst2Machine.shape

    def getConfig(self):
        '''
        step1: 数据参数初始化
        :return:
        '''
        # 生成配置文件
        self.init_conf()
        # 读取配置文件
        cf = ConfigParser()
        config_path = "../conf/config.ini"
        section_name = "data_file_name"
        cf.read(config_path)

        app_interference = cf.get(section_name, "app_interference")
        app_resources = cf.get(section_name, "app_resources")
        instance_deploy = cf.get(section_name, "instance_deploy")
        machine_resources = cf.get(section_name, "machine_resources")
        return app_interference, app_resources, instance_deploy, machine_resources

    def init_conf(self):
        '''
        初始化配置文件
        :retur
        '''
        libs.save_conf.write()

    def sort_dynamic(self):
        print("ss")

    def pickInstance(self, instanceid):
        '''
        先将instance从部署的主机中删除,删除一行，释放资源
        :return:
        '''
        self.inst2Machine.pop(instanceid)

    def toMachine(self, instanceid, machineid, doCheck=True):
        '''
        检查互斥条件,然后把instance放入主机
        :param instanceid: 实例id
        :param machineid: 主机id
        :param doCheck: 是否检测资源限制
        :return: True和False
        '''
        appid = self.inst2Machine[self.inst2Machine["instanceid"] == instanceid]["appid"].values[0]
        if doCheck:
            # 检查互斥


            # 检查资源限制
            for i in range(self.k):
                if (
                                self.machineResourcesUsed[self.machineResourcesUsed["machineid"] == machineid].iloc[:,
                                i + 1].values[0] +
                                self.appResources[self.appResources["appid"] == appid].iloc[:, i + 1].values[0]
                            >
                            self.machineResources[self.machineResources["machineid"] == machineid].iloc[:,
                            i + 1].values[0]):
                    print("Resource Limit: instance: ", instanceid, ",", "machine:", machineid,
                          self.machineResourcesUsed[self.machineResourcesUsed["machineid"] == machineid].iloc[:,
                          i + 1].values[0], "+",
                          self.appResources[self.appResources["appid"] == appid].iloc[:, i + 1].values[0], " >",
                          self.machineResources[self.machineResources["machineid"] == machineid].iloc[:,
                          i + 1].values[0])
                    # 如果不符合则 return False
                    return False
        # instance占用资源
        for i in range(self.k):
            self.machineResourcesUsed[self.machineResourcesUsed["machineid"] == machineid].iloc[:, i + 1].values[0] += \
                self.appResources[self.appResources["appid"] == appid].iloc[:, i + 1].values[0]
        return True

    def run(self):
        '''

        :return:
        '''
        # 已经部署的instance
        deployed_Instance = self.inst2Machine.loc[pd.isna(self.inst2Machine["machineid"]) == False]
        count_deployed_Instance, col = deployed_Instance.shape
        deployed_Instance = deployed_Instance.reset_index(drop=True)

        # 将已经部署的instance放置到对应主机中，占用相应资源，这一块代码比java慢了太多
        for i in range(count_deployed_Instance):
            print(i)
            instanceid = deployed_Instance["instanceid"][i]
            machineid = deployed_Instance["machineid"][i]
            self.toMachine(instanceid, machineid, doCheck=False)

        # 先对已经部署的主机列表按照资源消耗进行排序

        # 先使用大主机，磁盘优先计算限制条件
        row1, col = self.inst2Machine.shape
        while row1 > 0:
            # 每部署一次，消耗一个主机
            for row2 in self.inst2Machine.itertuples():
                if row2.
                self.toMachine(row2)

            # 筛选未部署的
            self.inst2Machine = self.inst2Machine[self.inst2Machine["isdeploy"] == False]
            row, col = self.inst2Machine.shape
            self.inst2Machine = self.inst2Machine.reset_index(drop=True)
            j = j + 1

            print("已经部署：", 68219 - row, "剩余部署Instance数据：", row)
            print("已经消耗Machine主机数据：", j)
        print("部署方案前几条示意：", self.machineHasApp.head())
        libs.save_result.save_result(self.machineHasApp)

    def deployInstance(self):
        '''
        部署逻辑
        :return:
        '''
        pass


if __name__ == '__main__':
    print("------------开始部署啦--------------")
    start = time.time()
    scheduling = Scheduling()
    # 加载数据
    scheduling.loadData()
    # 开始调度
    scheduling.run()
    # 部署完事
    print("------------部署完啦--------------")
    end = time.time()
    print("总共耗时：", end - start, "秒")
