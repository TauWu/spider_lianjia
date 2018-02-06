# -*- coding:utf-8 -*-
# 获取链家网中所有的房源链接信息
# 1.采用广度优先遍历，在页码数量大于100（非正常用户操作）的情况下获取下一级的房源信息
# 2.将拼接好的URL存入到output文件夹中待用

import sys
sys.path.append("..")

import requests
from bs4 import BeautifulSoup
from .spider_page import headers
import re
import random, time

from ..cheat.random_proxies import CheatRequests

raw_url = "https://sh.lianjia.com/zufang/{busi_area}/"

def get_pages(busi_area):
    '''获取该区域/商圈下拥有的房间页数'''
    raw_text = requests.get(raw_url.format(busi_area=busi_area),headers=headers).text
    bs4 = BeautifulSoup(raw_text,"lxml")

    totalAmount = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-head clear"}).findChild("h2").findChild("span")
    page_amount = int(int(re.findall("<span>(.+)</span>", str(totalAmount))[0])/30) + 1
    
    return page_amount

def get_urls_page(page_text):
    '''获取筛选页面的所有房间URL'''
    url_template = "https://sh.lianjia.com/zufang/{url}.html"
    bs4 = BeautifulSoup(page_text, "lxml")
    urls = list()
    room_list = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-wrap"}).findChild("ul",{"class","house-lst"}).findChildren("li")
    if len(re.findall("list-no-data",str(room_list))) != 0:
        return urls
    for room_info in room_list:
        url_info = room_info.findChild("div",{"class","info-panel"}).findChild("h2").findChild("a",{"target":"_blank"})
        url = re.findall(""".+href=\"https://sh.lianjia.com/zufang/(.+).html\"""",str(url_info))[0]
        urls.append(url_template.format(url=url))
    return urls

def get_urls(busi_area):
    '''获取某一商圈内的所有房源URL'''
    page_amount = get_pages(busi_area)
    raw_select_url = "https://sh.lianjia.com/zufang/{busi_area}/pg{page}/"
    select_url_list = list()
    urls = list()
    for i in range(1,page_amount+1):
        select_url_list.append(raw_select_url.format(busi_area=busi_area, page=i))
 
    req = CheatRequests([select_url_list])

    contents = req.get_cheat_all_content

    for page_texts in contents:
        for page_text in page_texts:
            url_add = get_urls_page(str(page_text))
            print("本页房源数量：", len(url_add))
            urls+=url_add
    return urls

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

# 将迭代器中获取到的需要爬取的URL信息写入到文件中
def write_urls(url_list):
    with open("/data/code/yujian/spider_lianjia/output/urls.req","a+") as f_url:
        url_list = ["%s\n"%url for url in url_list]
        f_url.writelines(url_list) 

def create_urls(dic_list):
    for dic in dic_list:
        url_adds = get_urls(dic)
        print("%s有%d套房源"%(dic, len(url_adds)))
        write_urls(url_adds)

dic_list_all = ['xuhui', 'hongkou', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu', 'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian', 'beicai', 'biyun', 'caolu', 'chuansha', 'datuanzhen', 'geqing', 'gaohang', 'gaodong', 'huamu', 'hangtou', 'huinan', 'jinqiao', 'jinyang', 'kangqiao', 'lujiazui', 'laogangzhen', 'lingangxincheng', 'lianyang', 'nichengzhen', 'nanmatou', 'sanlin', 'shibo', 'shuyuanzhen', 'tangqiao', 'tangzhen', 'waigaoqiao', 'wanxiangzhen', 'weifang', 'xuanqiao', 'xinchang', 'yuqiao1', 'yangdong', 'yuanshen', 'yangjing', 'zhangjiang', 'zhuqiao', 'zhoupu', 'chunshen', 'gumei', 'hanghua', 'huacao', 'jinhui', 'jinganxincheng', 'jinhongqiao', 'longbai', 'laominhang', 'maqiao', 'meilong', 'pujiang1', 'qibao', 'shenzhuang', 'wujing', 'zhuanqiao', 'dahua', 'dachangzhen', 'gongfu', 'gongkang', 'gucun', 'gaojing', 'jiangwanzhen', 'luojing', 'luodian', 'songbao', 'songnan', 'shangda', 'tonghe', 'yuepu', 'yanghang', 'zhangmiao'] 

if __name__ == "__main__":
    pass
    # 获取商圈列表 由于一般情况下不会有变化，故设为常量
    # dic_list = get_dic_url()
    # print(dic_list)