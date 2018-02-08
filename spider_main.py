# -*- coding:utf-8 -*-

import time
import sys
import csv

from module.spider.select_url import create_select_house_info_file, create_select_house_info_db, dic_list_all, get_dic_url, get_pages
from module.spider.spider_page import create_house_info_db


def create_task(busi_area):
    '''创建任务 - 通过商圈名称确定下一步需要爬取的房源详情链接列表'''
    busi_area_out = busi_area[:]

    # 遍历检查传入的商圈的页面是否超过100页 - 链家当前对100页以后的商圈有反爬虫处理
    # for busi_area_single in busi_area:
    #     if get_pages(busi_area_single) > 100:
    #         a = input("商圈[%s]的页码数大于100，是否删除本商圈后继续运行？[Y/N]"%busi_area_single)
    #         if a.strip() == "Y":
    #             busi_area_out.remove(busi_area_single)
    #         else:
    #             raise ValueError("商圈[%s]页数超量，请检查后重新执行！"%busi_area_single)

    # if len(busi_area_out) == 0:
    #     raise ValueError("待爬取商圈数量为0 程序结束")

    create_select_house_info_db(busi_area_out)

def create_task_csv(csv_file):
    '''通过csv文件创建任务 - csv_file为商圈列表csv文件'''
    task = []
    with open(csv_file) as csvfile:
        tasks = csv.reader(csvfile)
        # 取第一行数据
        task = next(tasks)
    create_task(task)

def do_task():
    create_house_info_db(20)

if __name__ == "__main__":

    # 爬取task.csv中列出的区域房源信息
    if len(sys.argv) == 1:
        # python3 spider_main.py
        create_task_csv("task.csv")
        do_task()

    # 执行主程序携带一个操作参数
    elif len(sys.argv) == 2:
        # python3 spider_main.py [operation]
        
        operation = sys.argv[1].strip()

        # python3 spider_main.py do - 爬取./output/urls.req目录下所有url对应的房源详情列表
        if operation == "do":
            #TODO
            do_task()

        # python3 spider_main.py create - 默认从csv文件中获取待爬取的url列表
        elif operation == "create":
            create_task_csv("task.csv")

        # python3 spider_main.py spider - 从csv文件中获取待爬取的url列表 后 获取房源详情
        elif operation == "spider":
            create_task_csv("task.csv")
            do_task()

        # python3 spider_main.py all - 获取所有待爬取的url列表 后 获取房源详情
        elif operation == "all":
            create_task(dic_list_all)
            # do_task()

        # python3 spider_main.py all1 - 先获取所有商圈 后 获取所有待爬url 后 获取房源详情
        elif operation == "all1":
            dic_list = get_dic_url()
            print(dic_list)
            create_task(dic_list_all)
            do_task()
            
        # python3 spider_main.py test - 测试代码
        elif operation == "test":
            pass

        # python3 spider_main.py test1 - 测试代码 - IP代理多进程多线程测试 (由于调用频次限制 目前暂时不采用此方法)
        # 测试结果采用多进程对速度的提升没有显著的影响，因此暂时不采用这种方法
        elif operation == "test1":

            from module.cheat.random_proxies import CheatRequests

            req = CheatRequests([["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"],["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"]])
            req.get_cheat_all_content_process

        # python3 spider_main.py test1 - 测试代码 - IP代理多线程测试
        # 测试结果：使用协程的运行测速和使用多进程多线程速度在误差范围内 - 因此后期请求采用协程运行
        elif operation == "test2":

            from module.cheat.random_proxies import CheatRequests
            import re

            req = CheatRequests([["http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp","http://2017.ip138.com/ic.asp"]])
            content_list = req.get_cheat_all_content
            content_list = next(content_list)
            for content in content_list:
                content_compile = re.compile("<center>(.+)</center>")
                ip_info = re.findall(content_compile, content.decode("gb2312"))
                print(ip_info)

        # python3 spider_main.py test3 - 测试代码 - IP代理验证测试
        # 非并行测试脚本 - 仅用作测试IP代理是否正常工作
        elif operation == "test3":

            from util.web.proxies import ProxiesVaild

            vailld = ProxiesVaild(num=10)
            print("使用方法A检查IP地址...")
            ip_infos = vailld.vaild_proxies_a
            for ip_info in ip_infos:
                print(ip_info)

            vailld.clear_ip_info()

            print("使用方法B检查IP地址...")
            ip_infos = vailld.vaild_proxies_b
            for ip_info in ip_infos:
                print(ip_info)

        else:
            raise ValueError("没有这个操作")
    
    # 执行主程序带两个操作
    elif len(sys.argv) == 3:
        # python3 spider_main.py [operation] [argv1]

        operation = sys.argv[1].strip()
        argv1 = sys.argv[2].strip()

        # python3 spider_main.py create [argv] - 获取指定商圈待爬取的url列表
        if operation == "create":
            create_task([argv1])

        # python3 spider_main.py spider [argv] - 获取指定商圈待爬取的url列表 后 获取房源详情
        elif operation == "spider":
            create_task([argv1])
            do_task()

        else:
            raise ValueError("没有这个操作")

    else:
        raise ValueError("参数太多")