# -*- coding: utf-8 -*-
# 随机请求发送
# 策略：随机IP地址和随机UA交替使用

from .random_proxies import random_proxies
from .random_headers import random_headers
import requests
import re

from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout

def random_requests(url):
    # 发送随机请求将请求返回
    proxies=random_proxies()
    headers=random_headers()
    raw_req = requests.get(url, headers=headers, proxies=proxies, timeout=0.5)
    return raw_req

def test_requests():
    try:
        raw_req = random_requests("http://2017.ip138.com/ic.asp")
        if raw_req.status_code != 200:
            print("请求错误，代理失败")
        else:
            raw_text = raw_req.content
            try:
                raw_text = raw_text.decode("gb2312")
                info_compile = re.compile("<center>.+\[(.+)\]来自：(.+)</center>")
                info = re.findall(info_compile, raw_text)[0]
                print("*******", info)
            except UnicodeDecodeError:
                print("解码错误，代理失败")
            
    except ProxyError:
        print("请求错误，请检查代理")
    except (ConnectTimeout, ReadTimeout):
        print("请求超时，发起下一次请求")
    except Exception as e:
        print("未知错误，已忽略")