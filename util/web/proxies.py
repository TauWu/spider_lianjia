# -*- coding: utf-8 -*-

import requests
import bs4
import re

url = "http://www.xicidaili.com/nn"

headers = {
    "Accecpt":"text/html,application/xhtml+xml,application/xml",  
    "Accept-Encoding":"gzip,deflate,sdch",  
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",  
    "Referer":"http://www.xicidaili.com",  
    "User-Agent":"Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"  
}

def get_ip():
    # 获取代理IP池
    req = requests.get(url, headers=headers)
    bs = bs4.BeautifulSoup(req.text, "lxml")
    data = bs.find_all("td")
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  
    port_compile = re.compile(r"<td>(\d+)</td>")
    speed_compile = re.compile(r"<div class=\"bar\" title=\"(.+)秒\">")
    ip = re.findall(ip_compile, str(data))  
    port = re.findall(port_compile, str(data))
    speed = re.findall(speed_compile, str(data))
    ip_list = list()
    for i in zip(ip, port, speed):
        speed = float(i[2][:])
        if speed < 1.0:
            ip_list.append(":".join(i[:2]))
    return ip_list

def get_ip_file():
    # 获取代理IP池并写入文件
    with open("./output/proxies.list","a+") as proxy:
        ips = get_ip()
        for ip in ips:
            proxy.write("%s\n"%ip)

if __name__ == "__main__":
    print(get_ip())