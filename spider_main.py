#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

import time
import sys
import csv

from module.spider.select_url import create_select_house_info_file, create_select_house_info_db, dic_list_all, get_dic_url, get_pages
from module.spider.spider_page import create_house_info_db
from module.spider.spider_stat import create_house_stat_db

from util.common.logger import use_logger, base_info

@use_logger(level="info")
def start_process(msg):
    '''程序开始日志打印'''
    pass

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

def page_task(start=0,num=50):
    '''分批爬取数据库中存入的house_id对应的房间详情页面信息'''
    create_house_info_db(start=start, num=num)

def page_task_proc():
    '''开启多进程，本进程3000秒后执行 详情页面爬虫'''
    time.sleep(3000)
    start_process("开始详情页面爬虫进程")
    page_task()

def stat_task(start=0,num=50):
    '''分批爬取数据库中存入的house_id对应的统计接口信息'''
    create_house_stat_db(start=start, num=num)

def stat_task_proc():
    '''开启多进程，本进程3000秒后执行 统计接口爬虫'''
    time.sleep(3000)
    start_process("开始统计接口爬虫进程")
    stat_task()

def spider_proc(fromtype=0,busi_area=dic_list_all):
    '''多进程爬虫启动'''
    from multiprocessing import Process
    
    p_create = Process()
    # 从文件读取商圈列表
    if fromtype == 0:
        p_create = Process(target=create_task_csv, args=("task.csv",))
        start_process("开始从商圈读取的列表中创建房间")

    # 直接获取的商圈列表
    elif fromtype == 1:
        p_create = Process(target=create_task, args=(busi_area,))
        start_process("开始从默认全部列表中创建房间")
    
    else:
        raise ValueError("参数错误，程序结束！")

    p_page = Process(target=page_task_proc)
    p_stat = Process(target=stat_task_proc)

    p_create.start()
    p_page.start()
    p_stat.start()

if __name__ == "__main__":

    start_process("主进程开始")

    # 程序流程
    info = '''程序爬虫主要流程：

    1. 爬取筛选页面，筛选条件是筛选结果页数小于100的地标
    2. 爬取详情页面，从数据库头遍历
    3. 爬取统计接口，从数据库头遍历

spider_main 后置参数说明：

    - create 爬虫第一步
    - page 爬虫第二步
    - stat 爬虫第三步
    - all 串行执行第三步
    
    '''

    # python3 spider_main.py - 12 - 爬取task.csv中列出的区域房源信息
    if len(sys.argv) == 1:
        spider_proc()

    # 执行主程序携带一个操作参数
    elif len(sys.argv) == 2:
        # python3 spider_main.py [operation]
        
        operation = sys.argv[1].strip()

        # python3 spider_main.py create - 1 -  默认从csv文件中获取待爬取的商圈列表 后 执行第一步
        if operation == "create":
            create_task_csv("task.csv")

        # python3 spider_main.py page - 2 - 爬取房源详情列表
        elif operation == "page":
            #TAG 这里可以修改第二步爬虫的起始和并发量
            page_task(start=0,num=50)

        # python3 spider_main.py stat - 3 - 从头获取数据库中所有的房源统计信息
        elif operation == "stat":
            #TAG 这里可以修改第三步爬虫的起始和并发量
            stat_task(start=0,num=50)

        # python3 spider_main.py spider - 123 - 从csv文件中获取待爬取的商圈列表 后 执行第一步 后 获取房源详情 后 获取统计详情
        elif operation == "spider":
            spider_proc()

        # python3 spider_main.py all - 123 - 获取所有待爬取的商圈列表 后 执行第一步 后 获取房源详情 后 获取统计详情
        elif operation == "all":
            spider_proc(1)

        # python3 spider_main.py all1 - 123 - 先获取所有商圈 后 获取所有待爬url 后 获取房源详情 后 获取统计详情
        elif operation == "all1":
            dic_list = get_dic_url()
            base_info(str(dic_list))
            spider_proc(1,dic_list)
            
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
                ip_info = re.findall(content_compile, content[0].decode("gb2312"))
                base_info(str(ip_info))

        # python3 spider_main.py test3 - 测试代码 - IP代理验证测试
        # 非并行测试脚本 - 仅用作测试IP代理是否正常工作
        elif operation == "test3":

            from util.web.proxies import ProxiesVaild

            vailld = ProxiesVaild(num=10)
            base_info("使用方法A检查IP地址...")
            ip_infos = vailld.vaild_proxies_a
            for ip_info in ip_infos:
                base_info(str(ip_info))

            vailld.clear_ip_info()

            base_info("使用方法B检查IP地址...")
            ip_infos = vailld.vaild_proxies_b
            for ip_info in ip_infos:
                base_info(str(ip_info))

        else:
            raise ValueError("没有这个操作")
    
    # 执行主程序带两个操作
    elif len(sys.argv) == 3:
        # python3 spider_main.py [operation] [argv1]

        operation = sys.argv[1].strip()
        argv1 = sys.argv[2].strip()

        # python3 spider_main.py create [argv] - 1 - 获取指定商圈待爬取的商圈列表 后 执行第一步
        if operation == "create":
            create_task([argv1])

        # python3 spider_main.py page [argv] - 2 -  爬取房源详情信息 - 参数为并发量
        elif operation == "page":
            page_task(int(argv1))

        # python3 spider_main.py page [argv] - 3 -  爬取房源统计信息 - 参数为并发量
        elif operation == "stat":
            stat_task(int(argv1))

        # python3 spider_main.py spider [argv] - 123 - 获取指定商圈待爬取的商圈列表 后 执行第一步 后 获取房源详情 后获取房源统计
        elif operation == "spider":
            spider_proc(1, [argv1])

        else:
            raise ValueError("没有这个操作")

    else:
        raise ValueError("参数太多")