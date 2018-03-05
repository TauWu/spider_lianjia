# -*- coding: utf-8 -*-
# 代理IP模块 通过切换不同的IP地址欺骗服务
# 策略：程序运行到0，10,20,30,40,50分时，向代理IP网站申请一批新的IP代理地址

from util.web.proxies import ProxiesRequests
from .random_headers import random_headers
from util.common.logger import use_logger

@use_logger(level="info")
def mureq_log(msg):
    pass

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
        self.content_list = []

    @property
    def get_cheat_first_content(self):
        '''运行第一个url列表 一般用作测试或者只有一个URL列表的情况'''
        self._urls = self.urlss[0]
        return self.req_content_list

    @property
    def get_cheat_all_content(self):
        '''运行所有的URL列表 *本请求为迭代请求，请注意网络IO压力*'''
        for urls in self.urlss:
            self._urls = urls
            mureq_log("即将请求%d条URL"%len(self._urls))
            yield self.req_content_list
            # 释放内存占用
            self._content = list()

    def get_cheat_all_content_process_base(self, urlss):
        ''' 多线程运行所有URL列表 *本请求为全量请求，请注意网络IO和内存压力*'''
        '''ATTENTION: 这里的urlss已经被get_cheat_all_content_process篡改，因此本函数只能被get_cheat_all_content_process调用'''
        import re
        self._urls = urlss
        self.content_list += self.req_content_list
        for content in self.content_list:
            print("########",re.findall("来自(.+)", str(content[0].decode('gb2312'))))
        return

    @property
    def get_cheat_all_content_process(self):
        '''多进程运行所有的URL列表 *本请求为迭代请求，请注意网络IO压力*'''
        from multiprocessing import Process, cpu_count
        from itertools import chain

        len_urlss = len(self.urlss)
        raw_urlss = self.urlss

        cpu_count = cpu_count()
        print("本机CPU核心数量为: %d"%cpu_count)
        
        # 将所有的任务拆分成CPU核心数量相同的份数
        urls_list = []
        length_urls_list = len_urlss / cpu_count + 1 # 每份任务的任务长度

        for i in range(0, cpu_count - 1):
            if i == cpu_count - 2:
                self.urlss = raw_urlss[int(i*length_urls_list):]
            else:
                self.urlss = raw_urlss[int(i*length_urls_list):int((i+1)*length_urls_list)]
            self.urlss = list(chain(*self.urlss))
            p = Process(target=self.get_cheat_all_content_process_base, args=(self.urlss,))
            p.start()