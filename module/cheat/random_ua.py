# -*- coding:utf-8 -*-
# 随机UA模块，程序发起请求时候使用随机的UA

def random_ua():
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    return headers