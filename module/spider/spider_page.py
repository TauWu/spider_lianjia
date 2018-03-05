# -*- coding: utf-8 -*-
# spider_page 页面数据分析

import sys
sys.path.append("../..")

from ..cheat.random_proxies import CheatRequests

from bs4 import BeautifulSoup
import re

from util.common.logger import use_logger, base_info

@use_logger(level="err")
def page_err(msg):
    pass

#TODO 后期请求附加参数将从cheat模块中获取
headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

# 房源特色图片tag枚举表
house_tag_detail = {
    "1":"床",
    "2":"电视",
    "3":"冰箱",
    "4":"洗衣机",
    "5":"空调",
    "6":"暖气",
    "7":"宽带",
    "9":"天然气",
    "10":"热水器",
    "11":"衣柜",
    "12":"桌椅",
    "13":"微波炉"
}

def get_house_info(page_text):
    '''筛选页面中所有需要的消息'''
    soup = BeautifulSoup(page_text, "lxml")
    house_info = list()

    # 获取房间编号
    try:
        house_id_soup = soup.findChild("span",{"class":"houseNum"})
    except AttributeError:
        page_err("BS解析错误%s"%page_text)
        return house_info
        
    house_id_compile = "([\dSH]+)"
    house_id = re.findall(house_id_compile, str(house_id_soup))
    if len(house_id) == 0:
        return house_info
    else:
        house_id = house_id[0]

    house_info.append(house_id)


    # 获取房间户型、发布时间
    lable_compile = re.compile("<i>(.+)</i>")
    result_compile = re.compile("</i>(.+)</p>")

    house_type_new = None
    sale_date_new = None
    house_type_new_soups = soup.findChildren("p",{"class":"lf"})
    for house_type_new_soup in house_type_new_soups:
        lable = re.findall(lable_compile, str(house_type_new_soup))[0]
        result = re.findall(result_compile, str(house_type_new_soup))[0]
        if lable.strip() == "房屋户型：":
            house_type_new = result
        if lable.strip() == "时间：":
            sale_date_new = result
    
    house_info.append(house_type_new)
    house_info.append(sale_date_new)

    # 获取基本属性
    basic_info_soup = soup.findChild("div",{"class":"introContent"}).findChild("div",{"class":"content"})
    basic_info_compile = "([^\x00-\xff]+)"
    basic_info = re.findall(basic_info_compile, str(basic_info_soup))
    basic_info = ",".join(basic_info)
    basic_info = basic_info.replace("：,","：")
    house_info.append(basic_info)

    # 获取房源标签
    house_tag_soups = soup.findChild("div",{"class":"zf-tag"}).findChildren("li")
    house_tag_list = list()
    house_tag_compile = "<li class=\"(.+)\">"
    for house_tag_soup in house_tag_soups:
        house_tag = re.findall(house_tag_compile, str(house_tag_soup))[0]
        if house_tag.find("tags") != -1:
            house_tag = house_tag[3:-5]
            house_tag_list.append(house_tag_detail[house_tag])

    house_info.append(",".join(house_tag_list))

    # 获取房源特色
    house_feature_soup = soup.findChild("div",{"class":"featureContent"})
    house_feature_compile = "([\u4e00-\u9fa5\d：]+)"
    house_feature = re.findall(house_feature_compile, str(house_feature_soup))
    house_feature = ",".join(house_feature)
    house_feature = house_feature.replace("：,","：")

    house_info.append(house_feature)

    return house_info

def get_house_infos(house_id_list):
    '''输入一个列表的house_id，返回所需要的房源信息'''
    url_template = "https://sh.lianjia.com/zufang/{house_id}.html"
    url_list = list()
    house_infos = list()

    # 获取待请求的URL列表
    for house_id in house_id_list:
        url_list.append(url_template.format(house_id=house_id))

    req = CheatRequests([url_list])

    contents = req.get_cheat_all_content

    for page_texts in contents:
        for page_text in page_texts:
            house_info = get_house_info(str(page_text[0].decode('utf-8')))
            if len(house_info) == 0:
                page_err("[IndexError]更新页面详情数据错误\tpage_text:%s"%str(page_text[0].decode('utf-8')).replace("\n",""))
                continue
                
            house_infos.append(house_info)

    return house_infos

def create_house_info_db(start=0,num=80):
    '''将获取到的房源详情的数据写入到数据库'''
    sys.path.append("../..")
    from module.database import LJDBController

    lj_db = LJDBController()

    house_id_lists = lj_db.get_house_ids(start=start, num=num)
    for house_id_list in house_id_lists:
        house_id_list_req = list()
        for house_id in house_id_list:
            house_id_list_req.append(house_id[0])
        s = get_house_infos(house_id_list_req)
        lj_db.update_house_info(s)

    lj_db.close

def create_house_info_redis(num=20):
    '''将Redis中缓存的需要重新跑批的房源重新爬虫'''
    sys.path.append("../..")
    from module.database import LJDBController
    from ..redis import LJRedisController

    base_info("开始从Redis内获取房源编号发起请求")

    rds = LJRedisController()
    lj_db = LJDBController()

    rds.failed_page_insert()

    house_list = rds.failed_page_get(num)

    for house_ids in house_list:
        house_id_list_req = list()
        for house_id in house_ids:
            house_id_list_req.append(house_id[1])
        s = get_house_infos(house_id_list_req)
        lj_db.update_house_info(s)
        rds.success_page_del(house_ids)

    lj_db.close
    rds.close

if __name__ == "__main__":
    create_house_info_db(num=20)
    # print(get_house_infos(["107100000682","107002262926","107001043986","SH0003283827"]))
