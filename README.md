# ServerManager

2018年阿里巴巴全球调度算法大赛项目

## 项目简单介绍
共约6K台宿主机（machine），包含了若干种型号，约68K个任务实例（instance），其中一部分已经部署在宿主机上，还有一部分没有被部署。

要求： 设计调度算法，在满足要求约束的前提下，通过将全部未被调度的任务实例调度到宿主机上以及腾挪部分已经部署的实例的方式，得到最优的部署方案。最优部署方案指实际使用宿主机数目尽可能少，且宿主机负荷不能过高。

项目地址：
https://tianchi.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.734b3b95rp1Lhx&raceId=231663

## python环境：
```angular2html

wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.2.0-Linux-x86_64.sh
yum install -y bzip2
yum install screen

vim .bashrc
export export PATH=/root/anaconda3/bin:$PATH

sh Anaconda3-5.2.0-Linux-x86_64.sh



```
## 运行：
```angular2html
#远程执行：
pip install -r requirementstxt

export PYTHONPATH=$PYTHONPATH:/root/ServerManager
ssh://liuyuqi@localhost:2201/home/liuyuqi/anaconda3/envs/py36/bin/python -u /home/liuyuqi/workspace/ServerManager/code/data_preview.py -dAgg

```

## 测试：
```angular2html

mvn package -Dmaven.test.skip=ture
java -cp AlibabaSchedulerEvaluator.jar com.aliyun.tianchi.mgr.evaluate.evaluate.file.evaluator.AlibabaSchedulerEvaluatorRun app_resources.csv machine_resources.csv instance_deploy.csv app_interference.csv result.csv

```