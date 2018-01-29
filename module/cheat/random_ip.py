# -*- coding: utf-8 -*-
# 代理IP模块 通过切换不同的IP地址欺骗服务
# 策略：程序运行到0，10,20,30,40,50分时，向代理IP网站申请一批新的IP代理地址

import sys
sys.path.append("../..")

from util.web.proxies import get_ip_file
import time
import random

# 获取随机IP
def random_ip():
    # 验证时间是否需要刷新IP代理池
    minsec = time.strftime("%M,%S", time.localtime())
    minsec = minsec.split(",")
    secs = int(minsec[1]) + 60 * int(minsec[0])
    if secs % 600 == 0:
        get_ip_file()
    proxies = list()
    with open("./output/proxies.list") as proxy:
        proxies = proxy.readlines()
    return proxies[random.randint(0,len(proxies)-1)][:-1]