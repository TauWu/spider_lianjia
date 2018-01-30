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

    def __init__(self, page):
        self.url = "http://www.xicidaili.com/nn/{page}".format(page=page)
        self.headers = {
            "Accecpt":"text/html,application/xhtml+xml,application/xml",  
            "Accept-Encoding":"gzip,deflate,sdch",  
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",  
            "Referer":"http://www.xicidaili.com",  
            "User-Agent":"Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"  
        }

    @property
    def _get_ip(self):
        # 获取代理IP池
        req = requests.get(self.url, headers=self.headers, timeout=1)
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
    def get_all(self):
        ip_lists = self._get_ip
        yield [ip_list.split(',') for ip_list in ip_lists]

    @property
    def get_ip(self):
        ip_lists = self._get_ip
        yield [ip_list.split(',')[0] for ip_list in ip_lists]

    @property
    def get_ip_port(self):
        ip_lists = self._get_ip
        yield [":".join(ip_list.split(',')[0:2]) for ip_list in ip_lists]
        

# ------------
# 数据库操作模块
# ------------

class DBController():

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


# ------------
# 数据库操作模块
# ------------

if __name__ == "__main__":
    db = DBController()

    sql_template = """
    insert into
        proxies_pool(ip, port, type)
    values
        ("%s", %s, "%s")
    """

    for page in range(1,10):
        IP = IPProxies(page)
        ip_list = next(IP.get_all)
        for ip in ip_list:
            sql = sql_template%(ip[0],ip[1],ip[2])
            try:
                db.execute(sql)
                print("插入IP【%s】成功"%ip[0])
            except db.IntegrityError:
                print("忽略插入重复【%s】"%"-".join(ip))
                pass
        time.sleep(5)
    
    db.close