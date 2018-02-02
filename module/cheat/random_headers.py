# -*- coding:utf-8 -*-
# 随机headers模块，程序发起请求时候使用随机的headers，主要是随机UA

from fake_useragent import UserAgent

default_headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def random_ua():
    ua = UserAgent()
    return ua.random

def random_headers():
    #TODO 验证该UA是否会对网页格式有影响
    default_headers["User-Agent"] = "%s"%(random_ua())
    return default_headers