# -*- coding:utf-8 -*-
# 获取链家网中所有的房源链接信息
# 1.采用广度优先遍历，在页码数量大于100（非正常用户操作）的情况下获取下一级的房源信息
# 2.将拼接好的URL存入到output文件夹中待用

import requests
from bs4 import BeautifulSoup
from .spider_page import headers
import re
import random, time
from util.common.logger import use_logger

from ..cheat.random_proxies import CheatRequests

raw_url = "https://sh.lianjia.com/zufang/{busi_area}/"

@use_logger(level="err")
def create_err(msg):
    pass

@use_logger(level="info")
def createinfo(msg):
    pass

def get_pages(busi_area):
    '''获取该区域/商圈下拥有的房间页数'''
    raw_text = requests.get(raw_url.format(busi_area=busi_area),headers=headers).text
    bs4 = BeautifulSoup(raw_text,"lxml")

    totalAmount = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-head clear"}).findChild("h2").findChild("span")
    page_amount = int(int(re.findall("<span>(.+)</span>", str(totalAmount))[0])/30) + 1
    
    return page_amount

def get_select_house_infos(page_text):
    '''获取筛选页面所有的 房间ID等信息'''
    get_data_compile = re.compile(r"([\u4e00-\u9fa50-9]+)")
    get_data_with_dot_compile = re.compile(r"([\u4e00-\u9fa50-9\.]+)")
    get_data_with_bracket_compile = re.compile(r"([\u4e00-\u9fa50-9\(\) )]+)")

    bs4 = BeautifulSoup(page_text, "lxml")
    select_house_infos = list()
    
    try:
        room_list = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-wrap"}).findChild("ul",{"class","house-lst"}).findChildren("li")
    except AttributeError:
        create_err("BS解析错误%s"%page_text)
        return select_house_infos

    if len(re.findall("list-no-data",str(room_list))) != 0:
        return select_house_infos
    for room_info in room_list:
        # 初始化列表中的房间信息
        select_house_info = []

        # 房源ID + 房源标题
        house_title_soup = room_info.findChild("div",{"class","info-panel"}).findChild("h2").findChild("a",{"target":"_blank"})
        house_title = list(re.findall(""".+href=\"https://sh.lianjia.com/zufang/(.+).html\"[\s\S]*title=\"(.+)\"""",str(house_title_soup))[0])

        # 第一行数据 商圈ID + 商圈名称 + 户型 + 面积 + 朝向
        where_soup = room_info.findChild("div",{"class":"col-1"}).findChild("div",{"class":"where"})
        # 获取商圈名称
        community_name_soup = where_soup.findChild("a").findChild("span", {"class":"region"})
        community_name_compile = re.compile("<span class=\"region\">(.+)</span>")
        community_name = re.findall(community_name_compile, str(community_name_soup))[0]

        # 获取where下的所有可利用资源
        where = re.findall(get_data_with_bracket_compile, str(where_soup))
        where = list(where)
        # 过滤单个的空格
        while True:
            try:
                where.remove(" ")
            except Exception:
                break
        # 拼接第一行数据
        where_list = []
        where_list.append(where[0])
        where_list.append(community_name)
        where_list += where[-3:]

        where = where_list

        # 第二行数据 行政区 + 楼层高低 + 楼层总数 + 建成时间
        other_soup = room_info.findChild("div",{"class":"col-1"}).findChild("div",{"class":"other"})
        other = re.findall(get_data_compile, str(other_soup))
        # 针对长风租房的防御
        if len(other) == 5:
            other = other[1:]
        # 针对没有建成时间的防御
        if len(other) == 3:
            other.append("")

        # 第三行数据 房源特色（list）
        extra_soup = room_info.findChild("div",{"class":"col-1"}).findChild("div",{"class":"view-label left"})
        extra = re.findall(get_data_with_dot_compile, str(extra_soup))

        # 带看人数
        square_soup = room_info.findChild("div",{"class":"col-2"}).findChild("span",{"class":"num"})
        square = re.findall(get_data_compile, str(square_soup))

        # 价格 + 创建时间
        price_soup = room_info.findChild("div", {"class":"col-3"}).findChild("span",{"class":"num"})
        price = re.findall(get_data_compile, str(price_soup))
        create_soup = room_info.findChild("div", {"class":"col-3"}).findChild("div",{"class":"price-pre"})
        create = re.findall(get_data_with_dot_compile, str(create_soup))

        # 拼接好的列表中的房源信息
        select_house_info = house_title + where + other + square + price + [create[0].replace(".","-")] + [";".join(extra)]
        select_house_infos.append(select_house_info)

    return select_house_infos

def get_select_house_infoss(busi_area):
    '''获取某一商圈内的所有房源的基础信息（从筛选页面中获取）'''
    page_amount = get_pages(busi_area)
    raw_select_url = "https://sh.lianjia.com/zufang/{busi_area}/pg{page}/"
    select_url_list = list()
    select_house_infoss = list()

    # 生成筛选商圈的URL列表
    for i in range(1,page_amount+1):
        select_url_list.append(raw_select_url.format(busi_area=busi_area, page=i))
 
    req = CheatRequests([select_url_list])

    contents = req.get_cheat_all_content

    for page_texts in contents:
        for page_text in page_texts:
            select_house_infos = get_select_house_infos(str(page_text[0].decode("utf-8")))
            createinfo("本页房源数量：%d"%len(select_house_infos))
            select_house_infoss+=select_house_infos

    return select_house_infoss

def get_dic_url():
    '''获取上海目录下小于100页的商圈拼音（用于拼接URL）'''
    req_url = raw_url.format(busi_area="")
    req = CheatRequests([[req_url]])
    content = req.get_cheat_first_content[0].decode("utf-8")
    bs = BeautifulSoup(content, "lxml")
    dic_list = bs.findChild("div",{"class":"filter-box"}).findChild("div",{"id":"filter-options"}).findChild("dl",{"class":"dl-lst clear"}).findChild("dd").findChild("div",{"class":"option-list"}).findChildren("a")
    dic_list = [re.findall("href=\"/zufang/(.+)/\"",str(dic))[0] for dic in dic_list[1:]]

    # 保证每个地标中包含的页码数量小于100页
    busi_list_result = []
    dic_list_result = dic_list[:]
    for dic in dic_list:
        pages = get_pages(dic)
        if get_pages(dic) > 100:
            # 删除超过100页的内容
            dic_list_result.remove(dic)
            req_url = raw_url.format(busi_area=dic)
            req = CheatRequests([[req_url]])
            content = req.get_cheat_first_content[0].decode("utf-8")
            bs = BeautifulSoup(content, "lxml")
            busi_list = bs.findChild("div",{"class":"filter-box"}).findChild("div",{"id":"filter-options"}).findChild("dl",{"class":"dl-lst clear"}).findChild("dd").findChild("div",{"class":"option-list sub-option-list"}).findChildren("a")
            busi_list = [re.findall("href=\"/zufang/(.+)/\"",str(busi))[0] for busi in busi_list[1:]]
            busi_list_result += busi_list
    dic_list_result += busi_list_result
    return dic_list_result

# 将迭代器中获取到的房源基础信息写入到select_house_info.req文件中去
def write_select_house_info(select_house_infos):
    with open("/data/code/yujian/spider_lianjia/output/select_house_info.req","a+") as f_info:
        select_house_infos = ["%s\n"%select_house_info for select_house_info in select_house_infos]
        f_info.writelines(select_house_infos) 

# 将筛选页面中的房源基础信息写入到select_house_info.req文件中去
def create_select_house_info_file(dic_list):
    for dic in dic_list:
        select_house_infos = get_select_house_infoss(dic)
        createinfo("%s有%d套房源"%(dic, len(select_house_infos)))
        write_select_house_info(select_house_infos)

# 将筛选页面中的房源基础信息写入到数据库中
def create_select_house_info_db(dic_list):
    from module.database import LJDBController

    lj_db = LJDBController()

    for dic in dic_list:
        select_house_infos = get_select_house_infoss(dic)
        createinfo("%s有%d套房源"%(dic, len(select_house_infos)))
        lj_db.insert_house(dic, select_house_infos)
    
    lj_db.close

dic_list_all = ['xuhui', 'hongkou', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu', 'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian', 'beicai', 'biyun', 'caolu', 'chuansha', 'datuanzhen', 'geqing', 'gaohang', 'gaodong', 'huamu', 'hangtou', 'huinan', 'jinqiao', 'jinyang', 'kangqiao', 'lujiazui', 'laogangzhen', 'lingangxincheng', 'lianyang', 'nichengzhen', 'nanmatou', 'sanlin', 'shibo', 'shuyuanzhen', 'tangqiao', 'tangzhen', 'waigaoqiao', 'wanxiangzhen', 'weifang', 'xuanqiao', 'xinchang', 'yuqiao1', 'yangdong', 'yuanshen', 'yangjing', 'zhangjiang', 'zhuqiao', 'zhoupu', 'chunshen', 'gumei', 'hanghua', 'huacao', 'jinhui', 'jinganxincheng', 'jinhongqiao', 'longbai', 'laominhang', 'maqiao', 'meilong', 'pujiang1', 'qibao', 'shenzhuang', 'wujing', 'zhuanqiao', 'dahua', 'dachangzhen', 'gongfu', 'gongkang', 'gucun', 'gaojing', 'jiangwanzhen', 'luojing', 'luodian', 'songbao', 'songnan', 'shangda', 'tonghe', 'yuepu', 'yanghang', 'zhangmiao'] 

if __name__ == "__main__":
    pass
    # 获取商圈列表 由于一般情况下不会有变化，故设为常量
    # dic_list = get_dic_url()
    # print(dic_list)