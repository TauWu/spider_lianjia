# -*- coding: utf-8 -*-

from proxies import IPDBController, IPProxies, IPVaildator
import time

def proxies_generator(start=1, end=2, sleep=5):
    """IP代理生成器"""

    db = IPDBController()
    IP = IPProxies(start=start,end=end)
    
    ip_lists = IP.ip_port_list

    for ip_lists in ip_lists:
        ip_list = ip_lists
        db.insert_ip(ip_list)
        print("页面爬取请求延迟%ds..."%sleep)
        time.sleep(sleep)

def proxies_gainer(method=0, limit=10):
    """IP代理获取器
    #### method
    + 0 | 查询限制条件下可用的代理列表
    + 1 | 查询可用的代理列表
    + 2 | 查询限制条件下有风险的代理列表
    + 3 | 查询有风险的代理列表
    
    """
    db = IPDBController()
    result = tuple()
    if method == 0:
        # 查询限制条件下可用的代理列表
        result = db.available_proxies(limit)
    elif method == 1:
        # 查询可用的代理列表
        result = db.available_proxies_full
    elif method == 2:
        # 查询限制条件下有风险的代理列表
        result = db.risk_proxies(limit)
    elif method == 3:
        # 查询有风险的代理列表
        result = db.risk_proxies_full
    else:
        print("没有这种方法")

    return result

def proxies_validator():
    """IP代理验证器"""
    vld = IPVaildator()
    return vld.test_requests()

if __name__ == "__main__":
    proxies_validator()