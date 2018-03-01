# -*- coding: utf-8 -*-

import requests
import bs4
import re

class IPProxies():
    """
    IP代理抓取模块

    可访问成员（函数）：
    - db
    - ip_port_list
    - ip_list

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
        self._conn = pymysql.connect(host=host,port=port,user=user, passwd=passwd,db=db,charset='utf8')
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
    - insert_ip()
    - available_proxies()
    - available_proxies_full
    - risk_proxies()
    - risk_proxies_full
    - available_count
    - risk_count
    - available_list
    - risk_list

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
        self.__available_proxies_sql_template__ = """
        select 
            id, ip, port, type 
        from 
            proxies_pool 
        where 
            deleted = 0 {failed_query}
        {limit_query}
        """

    def insert_ip(self, ip_port_list):
        """向IP数据库中插入一页的IP代理数据"""
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

    def available_proxies(self, limit=100, failed=0):
        """获取可用的代理列表基本方法"""
        limit_query = ""
        if limit > 0:
            # 如果限制小于0意味着由available_proxies_full调用
            limit_query = "limit %d"%limit
        # 有一定失败次数的控制
        failed_query = "and failed <= %d"%failed

        available_proxies_sql = self.__available_proxies_sql_template__.format(limit_query=limit_query, failed_query=failed_query)
        DBController.execute(self, available_proxies_sql)
        result = self.cur.fetchall()
        DBController.close

        return result

    @property
    def available_proxies_full(self):
        """获取所有可用的代理列表"""
        return self.available_proxies(limit=-1)

    def risk_proxies(self, limit=100):
        """获取限制的所有风险的代理列表　failed次数最多为５"""
        return self.available_proxies(limit, failed=5)

    @property
    def risk_proxies_full(self):
        """获取所有风险的代理列表 failed次数最多为５"""
        return self.available_proxies(limit=-1, failed=5)

    @property
    def available_list(self):
        """可用IP代理ID列表"""
        return [proxies[0] for proxies in self.available_proxies_full]

    @property
    def risk_list(self):
        """风险IP代理ID列表"""
        return [proxies[0] for proxies in len(self.risk_proxies_full)]

    @property
    def available_count(self):
        """可用IP代理个数"""
        return len(self.available_list)

    @property
    def risk_count(self):
        """可用IP代理个数"""
        return len(self.risk_list)

class IPVaildator(IPDBController):
    """
    IP代理验证器模块

    可访问成员（函数）：

    """
    def __init__(self):
        from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout
        from fake_useragent import UserAgent
        
        IPDBController.__init__(self)
        self.ProxyError = ProxyError
        self.ConnectTimeout = ConnectTimeout
        self.ReadTimeout = ReadTimeout
        self.ua = UserAgent()
        self.__headers__ = {}
        self.__proxies__ = {}

    def test(self):
        return IPDBController.available_list(self)

    def test_requests(self):

        ip_port_list = self.available_proxies_full
        for ip_port in ip_port_list:
            try:
                self.__headers__["User-Agent"] = self.ua.random
                self.__proxies__ = {}
                # self.__proxies__[ip_port[3].lower()] = ":".join(ip_port[1:3])
                self.__proxies__["http"] = "%s://%s"%(ip_port[3].lower(), ":".join(ip_port[1:3]))
                self.__proxies__["https"] = "%s://%s"%(ip_port[3].lower(), ":".join(ip_port[1:3]))
                raw_req = requests.get("http://2017.ip138.com/ic.asp", headers=self.__headers__, proxies=self.__proxies__,timeout=2)
                
                if raw_req.status_code != 200:
                    print("请求错误，代理失败")
                else:
                    raw_text = raw_req.content
                    try:
                        raw_text = raw_text.decode("gb2312")
                        info_compile = re.compile(r"<center>您的IP是：\[(.+)\] 来自：(.+)</center>")
                        info = re.findall(info_compile, raw_text)
                        print("*******", info, ip_port[3])
                    except UnicodeDecodeError:
                        print("解码错误，代理失败")
                    
            except self.ProxyError:
                print("请求错误，请检查代理")
            except (self.ConnectTimeout, self.ReadTimeout):
                print("请求超时，发起下一次请求")
            except Exception:
                print("未知错误，已忽略")