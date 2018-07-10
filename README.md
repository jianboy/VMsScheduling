# ServerManager

2018年阿里巴巴全球调度算法大赛项目


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
