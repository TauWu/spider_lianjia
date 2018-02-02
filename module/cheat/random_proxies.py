# -*- coding: utf-8 -*-
# 代理IP模块 通过切换不同的IP地址欺骗服务
# 策略：程序运行到0，10,20,30,40,50分时，向代理IP网站申请一批新的IP代理地址

import sys
sys.path.append("../..")

from util.web.proxies import ProxiesRequests
from .random_headers import random_headers

class CheatRequests(ProxiesRequests):
    '''
    欺骗请求模块

    '''
    def __init__(self, urlss):
        '''urlss 即为urls列表的列表 可以在这里启用多进程'''
        self.urlss = urlss
        #TODO 这里可能要添加一下Cookie
        ProxiesRequests.__init__(self)
        self.add_headers(random_headers())

    @property
    def get_cheat_first_content(self):
        '''运行第一个url列表 一般用作测试或者只有一个URL列表的情况'''
        self._urls = self.urlss[0]
        return self.req_content_list