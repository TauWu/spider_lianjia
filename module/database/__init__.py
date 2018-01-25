# -*- coding: utf-8 -*-

## 这一级目录下需要有一个数据库配置文件 config.py

# 待连接数据库基础信息

'''
database_info = {
    "host":"localhost",
    "port":3306,
    "user":"user",
    "passwd":"passwd",
    "db":"database",
    "charset":"utf8"
}
'''

import pymysql
from .config import database_info

def db_conn():
    # 数据库连接方法
    conn = pymysql.connect(host=database_info["host"],port=database_info["port"],user=database_info["user"],passwd=database_info["passwd"],db=database_info["db"],charset=database_info["charset"])
    cur = conn.cursor()
    return conn, cur