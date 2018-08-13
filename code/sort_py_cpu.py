#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
对instance数据按照cpu使用率降序排列
@Auther :liuyuqi.gov@msn.cn
@Time :8/13/2018 9:04 PM
@File :sort_py_cpu.py
'''
import pandas as pd

res = pd.DataFrame()

appResources = pd.read_csv("../resb/app_resources.csv", header=None,
                           names=list(["appid", "cpu", "mem", "disk", "P", "M", "PM"]), encoding="utf-8")
instanceDeploy = pd.read_csv("../resb/instance_deploy.csv", header=None,
                             names=list(["instanceid", "appid", "machineid"]), encoding="utf-8")
instanceDeploy["cpu_avg"] = None
tmp_cpu = appResources["cpu"].str.split('|', expand=True).astype('float')
appResources["cpu_avg"] = tmp_cpu.T.mean().T
h, l = instanceDeploy.shape
print(h)
# for i in range(0, h):
#     instanceDeploy["cpu_avg"][i] = appResources[appResources["appid"] == instanceDeploy["appid"][i]]["cpu_avg"].values[
#         0]
#     if i % 1000==0:
#         print(i)
# res["instanceid"] = instanceDeploy["instanceid"]
# res["cpu"] = instanceDeploy["cpu_avg"]
# res.sort_values(ascending=False, by="cpu", inplace=True)
#
# res.to_csv("../resb/app_cpu.csv", index=False, header=False)
