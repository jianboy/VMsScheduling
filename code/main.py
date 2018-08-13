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

import utils.save_conf
import utils.save_result


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
    num_app = num_inst = num_mac = 0
    num_k = 200
    cpuIter = list()
    appIndex = {}
    machineIndex = {}
    inst2AppIndex = {}

    # apps = list()
    # machines = list()
    appResources = list()  # app表，
    machineResources = list()  # machine表
    instanceDeploy = list()  # instance表
    appInterference = list()  # app_interfence冲突表

    # 动态数据
    inst2MachineRemine = {}
    machineResourcesUsed = list()
    machineHasApp = list()  # 6000 [{}, {},{6004=1, 9126=1, 1598=1}, {}, {}, {},
    inst2Machine = list()
    result = pd.DataFrame(columns=list(["instanceid", "machineid"]), data=list())

    def __init__(self, **kw):
        '''
        初始化参数
        :param kw:
        '''
        for k, v in kw.items():
            setattr(self, k, v)

    def loadData(self):
        for i in range(self.T):
            self.cpuIter.append(i)
        app_interference, app_resources, instance_deploy, machine_resources = self.getConfig()
        # 1.app_resources 9338*201
        self.appResources = pd.read_csv(app_resources, header=None,
                                        names=list(["appid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
        tmp_cpu = self.appResources["cpu"].str.split('|', expand=True).astype('float')
        tmp_mem = self.appResources["mem"].str.split('|', expand=True).astype('float')
        for i in range(self.T):
            self.appResources["cpu_" + str(i)] = tmp_cpu[i]
            self.appResources["mem_" + str(i)] = tmp_mem[i]
        # 去掉cpu/men两列
        self.appResources.pop("cpu")
        self.appResources.pop("mem")
        self.num_app, col = self.appResources.shape  # 9338*201 201列：appid,cpu_1,cpu_2,...mem_1,men_2....,P,M,PM
        self.appResources["appid"] = pd.to_numeric(self.appResources["appid"].str.split("_", expand=True)[1].values)

        # 2.machine_resources 6000*201
        self.machineResources = pd.read_csv(machine_resources, header=None, names=list(
            ["machineid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
        self.num_mac, col = self.machineResources.shape
        for i in range(self.T):
            self.machineResources["cpu_" + str(i)] = self.machineResources["cpu"]
            self.machineResources["mem_" + str(i)] = self.machineResources["mem"]
        self.machineResources.pop("cpu")
        self.machineResources.pop("mem")
        self.machineResources["machineid"] = pd.to_numeric(
            self.machineResources["machineid"].str.split("_", expand=True)[1].values)
        self.machineResourcesUsed = self.machineResources.copy()
        for i in range(200):
            self.machineResourcesUsed.iloc[:, i + 1] = 0
        # 初始化 6000个空字典组成的list[{},{}....]
        for i in range(self.num_mac):
            self.machineHasApp.append({})

        # 3.instance_deploy
        self.instanceDeploy = pd.read_csv(instance_deploy, header=None,
                                          names=list(["instanceid", "appid", "machineid"]), encoding="utf-8")
        # 增加一个字段标注是否部署
        self.instanceDeploy["isdeploy"] = False
        self.instanceDeploy["instanceid"] = pd.to_numeric(
            self.instanceDeploy["instanceid"].str.split("_", expand=True)[1].values)
        self.instanceDeploy["appid"] = pd.to_numeric(self.instanceDeploy["appid"].str.split("_", expand=True)[1].values)
        self.instanceDeploy["machineid"] = pd.to_numeric(
            self.instanceDeploy["machineid"].str.split("_", expand=True)[1].values)

        # 4.app_interference 冲突表
        self.appInterference = pd.read_csv(app_interference, header=None,
                                           names=list(["appid1", "appid2", "max_interference"]), encoding="utf-8")
        self.appInterference["appid1"] = pd.to_numeric(
            self.appInterference["appid1"].str.split("_", expand=True)[1].values)
        self.appInterference["appid2"] = pd.to_numeric(
            self.appInterference["appid2"].str.split("_", expand=True)[1].values)

        # instance按照磁盘消耗排序
        self.num_app, col = self.appResources.shape
        self.num_inst, col = self.instanceDeploy.shape

    def getConfig(self):
        '''
        step1: 数据参数初始化
        :return:
        '''
        # 生成配置文件
        # self.init_conf()

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
        utils.save_conf.write()

    def sort_dynamic(self):
        print("ss")

    def pickInstance(self, instanceid):
        '''
        先将instance从部署的主机中删除,删除一行，释放资源
        :return:
        '''
        if instanceid not in self.inst2Machine["instance"]:
            return
        appid = self.inst2Machine[self.inst2Machine["instanceid"] == instanceid]["appid"].values[0]

        # 更新machineResourcesUsed
        for i in range(self.num_k):
            machineResourcesUsed[fromMachine][j] -= appResources[appIt][i]
        fromMachine = self.inst2AppIndex
        self.inst2Machine.pop(instanceid)

    def toMachine(self, instanceid, machineid, doCheck=False):
        '''
        检查互斥条件,然后把instance放入主机
        :rtype: object
        :param instanceid: 实例id
        :param machineid: 主机id
        :param doCheck: 是否检测资源限制
        :return: True和False
        '''
        # instanceid所属的appid
        appid = self.instanceDeploy[self.instanceDeploy["instanceid"] == instanceid]["appid"].values[0]
        # machineid从1开始，而index从0开始
        hasApp = self.machineHasApp[int(machineid - 1)]
        if doCheck:
            # 检查互斥


            # 检查资源限制
            for i in range(self.num_k):
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
        # 将inst放入新的machine,占用资源
        self.inst2Machine.append([{"instanceid": instanceid, "machineid": machineid}])
        if appid not in hasApp:
            hasApp.update({appid: 1})
        else:
            hasApp.update({appid: hasApp.get(appid) + 1})
        for i in range(self.num_k):
            self.machineResourcesUsed[self.machineResourcesUsed["machineid"] == machineid].iloc[:, i + 1].values[
                0] += \
                self.appResources[self.appResources["appid"] == appid].iloc[:, i + 1].values[0]
        return True

    def run(self, start):
        '''
        执行部署
        :return:
        '''
        # 已经部署的instance
        deployed_Instance = self.instanceDeploy.loc[pd.isna(self.instanceDeploy["machineid"]) == False]
        count_deployed_Instance, col = deployed_Instance.shape
        deployed_Instance.reset_index(drop=True, inplace=True)

        # 将已经部署的instance放置到对应主机中，占用相应资源，这一块代码比java慢了太多
        for i in range(count_deployed_Instance):
            instanceid = deployed_Instance["instanceid"][i]
            machineid = deployed_Instance["machineid"][i]
            self.toMachine(instanceid, machineid, doCheck=False)
            print("初始部署第", i, "个，持续耗时", time.time() - start, "秒")

        # 对instance同样按照disk消耗排序
        self.instanceDeploy = self.instanceDeploy.sort_values(ascending=False, by="disk")

        # 然后通过ff方法，把instance放入machine中。每次放入instance后，队列删除，每次消耗主机i，删除主机i.先使用大主机，磁盘优先计算限制条件
        row1, col = self.instanceDeploy.shape
        while row1 > 0:
            # 先对主机列表按照disk剩余进行排序，降序
            self.machineResourcesUsed = self.machineResourcesUsed.sort_values(ascending=False, by="disk")

            # 每部署一次，消耗一个主机
            self.deployInstance()
            # 筛选未部署的
            self.instanceDeploy = self.instanceDeploy[self.instanceDeploy["isdeploy"] == False]
            row, col = self.instanceDeploy.shape
            self.instanceDeploy.reset_index(drop=True, inplace=True)
            j = j + 1

            print("已经部署：", 68219 - row, "剩余部署Instance数据：", row)
            print("已经消耗Machine主机数据：", j)
        print("部署方案前几条示意：", self.result.head())
        utils.save_result.save_result(self.result)

    def dcmp(self, x):
        '''
        将结果映射到-1，0，1
        :param x:
        :return:
        '''
        if abs(x) < 1e-9:
            return 0
        elif x > 0:
            return 1
        else:
            return -1

    def deployInstance(self):
        '''
        部署逻辑
        :return:
        '''
        # 主机：self.machineResourcesUsed["machineid"][0]
        for row in self.instanceDeploy.itertuples():
            i = row.Index
            # 当前row实例尝试部署到新主机，如果可以部署则部署，如果初始已经部署，则算迁移，释放原来主机资源
            if self.toMachine(row, machineid="", doCheck=True):
                machineHasApp = machineHasApp.append(pd.DataFrame(
                    [{"instanceid": row.instanceid,
                      "machineid": "machine_" + str(j)}]))


if __name__ == '__main__':
    print("------------开始部署啦--------------")
    start = time.time()
    scheduling = Scheduling()
    # 加载数据
    scheduling.loadData()
    print("加载数据耗时:", time.time() - start)
    # 开始调度
    scheduling.run(start)
    # 部署完事
    print("------------部署完啦--------------")
    end = time.time()
    print("总共耗时：", end - start, "秒")
