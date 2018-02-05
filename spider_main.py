# -*- coding:utf-8 -*-

import time
import sys
import csv

from module.spider.select_url import create_urls
from module.spider.spider_page import getHouseInfo

from module.cheat.random_proxies import CheatRequests

from util.database.insert import insert_lianjia_house_json
from util.web.proxies import ProxiesVaild

# 通过文件来中转 监控程序运行情况
def create_task(busi_area):
    create_urls(busi_area)

# 读取文件内部URL以发起请求
def do_task_csv():
    with open("./output/result.csv","a+") as result:
        result.write("编号,价格,户型,面积,楼层,朝向,行政区,商圈,上线日期,地标名称,地标地址\n")
    with open("./output/urls.req","r") as f:
        urls = f.readlines()
        if len(urls) != 0:
            for url in urls:
                info = getHouseInfo(url[:-1])
                with open("./output/result.csv","a+") as result:
                    result.write(str(info))
                    result.write("\n")
                time.sleep(0.3)

        else:
            print("urls.req文件为空，请检查")


def do_task():
    with open("./output/urls.req","r") as f:
        urls = f.readlines()
    if len(urls) != 0:
        for url in urls:
            info = getHouseInfo(url[:-1])
            insert_lianjia_house_json(info)
            

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # python3 spider_main.py
        # 爬取task.csv中列出的区域房源信息
        with open("task.csv") as csvfile:
            tasks = csv.reader(csvfile)
            for task in tasks:
                create_task(task)
                do_task()

    elif len(sys.argv) >= 2:

        operation = sys.argv[1].strip()
        if len(sys.argv) == 2:
            Argv = ""
        else:
            Argv = sys.argv[2].strip()

        if operation == "create":
        # python3 spider_main.py create
            if Argv == "":
                Argv = input("请输入待爬取商圈的拼音")
                if Argv == "":
                    confirm = input("即将爬取链家网当前所有在售房源URL，请确定。（Y/N）")
                    if confirm.strip() == "Y":
                        create_task([Argv])
                else:
                    create_task([Argv])
            else:
                create_task([Argv])

        elif operation == "do":
        # python3 spider_main.py do
            with open("./output/urls.req") as urls:
                if len(urls.readlines()) == 0:
                    print("./output/urls.req 文件为空，请检查！")
            do_task()

        elif operation == "all":
        # python3 spider_main.py all
            confirm = input("即将爬取链家网当前所有房源，请确定。（Y/N）")
            #TODO 下一版需要爬取所有的房源消息包括表面不能搜索到的
            if confirm.strip() == "Y":
                create_task([""])
                do_task()
        
        elif operation == "test":
        # python3 spider_main.py test
            req = CheatRequests([["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"]])
            # req = CheatRequests([["https://sh.lianjia.com/zufang/"]])
            # for content in req.get_cheat_all_content:
            #     print(content)
            #     time.sleep(5)
            req.get_cheat_all_content_process
