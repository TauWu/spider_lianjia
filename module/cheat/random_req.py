# -*- coding: utf-8 -*-
# 随机请求发送
# 策略：随机IP地址和随机UA交替使用

from .random_ip import random_ip
from .random_ua import random_ua
import requests

def requests(url):
    requests.get(url, proxies=random_ip, headers=random_ua)