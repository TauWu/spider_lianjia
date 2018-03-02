#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# 安装配置环境时执行的程序

from util.common.logger import base_info


# 基础设置
info = """
安装一台新服务器需要对本程序的环境进行配置：
具体操作如下：
1. 代理设置配置 => ./util/web/config.py
2. 数据库设置配置 => ./module/database/config.py
---

是否按顺序全部配置？（Y/N）

"""

operator_info = """
请选择你需要配置的文件对应的数字：
【0】 退出程序
【1】 代理文件设置
【2】 数据库文件设置
---
"""

# 代理设置配置文件模板
proxy_config_template = """
# -*- coding: utf-8 -*-

#
# 这里存放有关的配置文件
#

# constant 需要迁移走
orderno = "{orderno}"
secret = "5a6fee02149541d18b6e70de5059538b"
ip_port = "forward.xdaili.cn:80"
raw_url = "http://2017.ip138.com/ic.asp"

"""

db_config_template = """
database_info = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "passwd":"%s",
    "db":"spider_data",
    "charset":"utf8"
}
"""

def proxy_config():
    '''代理程序设置'''

    orderno = input("请输入转发请求代理订单号！")
    base_info("配置代理请求转发成功！")
    with open("./util/web/config.py","w") as config:
        config.writelines(proxy_config_template.format(orderno=orderno))

def database_config():
    '''数据库设置'''

    passwd = input("请输入本机数据库root密码！")
    base_info("配置数据库密码成功！")
    with open("./module/database/config.py","w") as config:
        config.writelines(db_config_template%passwd)

if __name__ == "__main__":

    base_info("开始配置一台新机器...")

    yorn = input(info)

    # 按照顺序配置所有文件
    if yorn.strip() == "Y":
        proxy_config()
        database_config()

    # 用户手动选择需要配置的文件
    elif yorn.strip() == "N":

        while True:

            operator = input(operator_info)

            if operator.strip() == "0":
                print("设置文件配置程序退出...")
                break
            
            elif operator.strip() == "1":
                proxy_config()
            
            elif operator.strip() == "2":
                database_config()

            else:
                continue

    else:
        raise ValueError("没有该选项！")