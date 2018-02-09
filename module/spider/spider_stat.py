# -*- coding: utf-8 -*-
# spider_stat 统计接口分析

import sys
sys.path.append("..")

from ..cheat.random_proxies import CheatRequests

from bs4 import BeautifulSoup
import re, json

def get_house_stat(house_stat_json):
    house_stat_dict = json.loads(house_stat_json)

    code = house_stat_dict["code"]

    if code == 1:
        # 地标经纬度
        try:
            position = house_stat_dict["data"]["resblockPosition"]
        except KeyError:
            position = "0,0"
        # 带看指标
        try:
            see_stat_total = int(house_stat_dict["data"]["seeRecord"]["totalCnt"])
        except KeyError:
            see_stat_total = -1

        try:
            see_stat_weekly = int(house_stat_dict["data"]["seeRecord"]["thisWeek"])
        except KeyError:
            see_stat_weekly = -1
        
        # 地标指标
        try:
            community_sold_count =len(house_stat_dict["data"]["resblockSold"])
        except KeyError:
            community_sold_count = -1

        # 商圈指标
        try:
            busi_sold_count = len(house_stat_dict["data"]["bizcircleSold"])
        except KeyError:
            busi_sold_count = -1

    else:
        print("接口获取错误！")

    # 以下是需要的数据

    return list((position, see_stat_total, see_stat_weekly, community_sold_count, busi_sold_count, str(house_stat_json)))

def get_house_stats(hc_id_list):
    '''输入一个列表的house_id+community_id，返回需要的房源统计借口信息'''
    url_template = "https://sh.lianjia.com/zufang/housestat?hid={house_id}&rid={community_id}"
    url_list = list()
    house_stat_list = list()

    # 获取待请求的URL列表
    for hc_id in hc_id_list:
        url_list.append(url_template.format(house_id=hc_id[0], community_id=hc_id[1]))
    
    req = CheatRequests([url_list])

    contents = req.get_cheat_all_content

    for house_stats in contents:
        for house_stat in house_stats:
            house_stat_info = get_house_stat(str(house_stat[0].decode("unicode-escape").replace(r"\/","/")))
            house_stat_detail = [re.findall("([SH\d]+)",house_stat[1])[0]]
            house_stat_detail += house_stat_info
            house_stat_list.append(tuple(house_stat_detail))

    return house_stat_list

def create_house_stat_db(start=0,num=80):
    '''将获取到的房源统计信息写入到数据库'''
    sys.path.append("../..")
    from util.database import LJDBController

    lj_db = LJDBController()
    hc_id_lists = lj_db.get_hc_ids(start=start, num=num)
    for hc_id_list in hc_id_lists:
        hc_id_list_req = list()
        for hc_id in hc_id_list:
            hc_id_list_req.append(hc_id)
        s = get_house_stats(hc_id_list_req)
        lj_db.update_house_stat(s)

    lj_db.close

if __name__ == "__main__":
    create_house_stat_db(num=2)



