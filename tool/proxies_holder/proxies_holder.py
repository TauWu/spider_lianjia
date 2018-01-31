# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import requests
import bs4
import re
import time


# ------------
# IP代理抓取模块
# ------------

class IPProxies():
    """
    IP代理抓取模块

    可访问成员（函数）：
    - start

    """

    def __init__(self, start=1, end=2):
        #TODO 参数检查
        self.__raw_url__ = "http://www.xicidaili.com/nn/{page}"
        self.__start__ = start
        self.__end__ = end
        self.__headers__ = {
            "Accecpt":"text/html,application/xhtml+xml,application/xml",  
            "Accept-Encoding":"gzip,deflate,sdch",  
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",  
            "Referer":"http://www.xicidaili.com",  
            "User-Agent":"Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"  
        }
        self.db = IPDBController()

    def __get_ip__(self, page):
        # 获取代理IP池
        url = self.__raw_url__.format(page=page)
        req = requests.get(url, headers=self.__headers__, timeout=1)
        bs = bs4.BeautifulSoup(req.text, "lxml")
        data = bs.find_all("td")
        
        # 获取需要的信息
        ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  
        port_compile = re.compile(r"<td>(\d+)</td>")
        speed_compile = re.compile(r"<div class=\"bar\" title=\"(.+)秒\">")
        type_compile = re.compile(r"<td>(HTT.+)</td>")

        ip = re.findall(ip_compile, str(data))  
        port = re.findall(port_compile, str(data))
        speed = re.findall(speed_compile, str(data))
        _type = re.findall(type_compile, str(data))

        ip_list = list()
        for i in zip(ip, port, _type, speed):
            speed = float(i[3][:])
            if speed < 1.0:
                ip_list.append(",".join(i[:3]))
        return ip_list

    @property
    def ip_port_list(self):
        for page in range(self.__start__, self.__end__):
            ip_lists = self.__get_ip__(page)
            # 返回一页的URL数据
            yield [ip_list.split(',') for ip_list in ip_lists]

    @property
    def ip_list(self):
        for page in range(self.__start__, self.__end__):
            ip_lists = self.__get_ip__(page)
            # 返回一页的URL数据
            yield [ip_list.split(',')[0] for ip_list in ip_lists]  

# ------------
# 数据库操作模块
# ------------

class DBController():
    """
    数据库操作模块
    
    可访问成员（函数）：
    - cur
    - IntegrityError
    - execute(sql)
    - close

    """

    def __init__(self, host="localhost", user="root", passwd="root", port=3306, db="spider_data"):
        import pymysql
        from pymysql.err import IntegrityError

        # 保护连接为私有成员
        self._conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        self.cur = self._conn.cursor()
        self.IntegrityError = IntegrityError

    def execute(self, SQL):
        # 执行一条SQL语句
        self.cur.execute(SQL)
        self._conn.commit()

    @property
    def close(self):
        # 关闭数据库连接
        self._conn.close()
        self.cur.close()


class IPDBController(DBController):
    """
    IP代理数据库操作模块

    可访问成员（函数）：
    - insert_ip(ip_port_list)

    """

    def __init__(self):
    # 初始化IPDBController对象
        DBController.__init__(self)
        self.__insert_sql_template__ = """
        insert into
            proxies_pool(ip, port, type)
        values
            ("{ip}", {port}, "{type}")
        """

    def insert_ip(self, ip_port_list):
    # 向IP数据库中插入一页的IP代理数据
        for ip_port in ip_port_list:
            print(ip_port)
            (ip, port, _type) = tuple(ip_port)
            insert_sql = self.__insert_sql_template__.format(ip=ip, port=port, type=_type)
            try:
                DBController.execute(self, insert_sql)
                print("插入IP【%s】成功"%ip)
            except self.IntegrityError:
                print("忽略插入重复【%s】"%"-".join(ip_port))
                pass

        DBController.close

# ------------
# IP代理检查模块
# 通过访问ip138验证
# ------------
# class IPVerify():

#     def __init__(self, timeout=1, ):

if __name__ == "__main__":
    # 创建一个插入IP代理的对象
    db = IPDBController()

    # 创建一个生成IP代理的对象
    IP = IPProxies(start=1,end=4)
    
    ip_lists = IP.ip_port_list

    for ip_lists in ip_lists:
        ip_list = ip_lists
        db.insert_ip(ip_list)
        print("页面爬取请求延迟10s...")
        time.sleep(10)