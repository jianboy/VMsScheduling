#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
注意文件名直接写 logging.py 会出错！所以说python文件命名都有规范！
@Auther :liuyuqi.gov@msn.cn
@Time :2018/7/8 13:09
@File :mlogging.py
'''

import logging

class Log():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')

    def debug(msg):
        logging.debug(msg)

    def info(msg):
        logging.info(msg)

    def warning(msg):
        logging.warning(msg)
