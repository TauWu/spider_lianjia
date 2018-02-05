# -*- coding:utf-8 -*-
# 获取链家网中所有的房源链接信息
# 1.采用广度优先遍历，在页码数量大于100（非正常用户操作）的情况下获取下一级的房源信息
# 2.将拼接好的URL存入到output文件夹中待用

import sys
sys.path.append("..")

import requests
from bs4 import BeautifulSoup
from spider_page import headers
import re
import random, time

from cheat.random_proxies import CheatRequests

raw_url = "https://sh.lianjia.com/zufang/{busi_area}/"

# 获取该区域/商圈下拥有的房间页数
def get_pages(busi_area):
    raw_text = requests.get(raw_url.format(busi_area=busi_area),headers=headers).text
    bs4 = BeautifulSoup(raw_text,"lxml")

    totalAmount = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-head clear"}).findChild("h2").findChild("span")
    page_amount = int(int(re.findall("<span>(.+)</span>", str(totalAmount))[0])/30) + 1
    
    return page_amount

# 获取筛选页面的所有房间URL
def get_urls_page(page_text):
    url_template = "https://sh.lianjia.com/zufang/{url}.html"
    bs4 = BeautifulSoup(page_text, "lxml")
    urls = list()
    room_list = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-wrap"}).findChild("ul",{"class","house-lst"}).findChildren("li")
    for room_info in room_list:
        url_info = room_info.findChild("div",{"class","info-panel"}).findChild("h2").findChild("a",{"target":"_blank"})
        url = re.findall(""".+href=\"https://sh.lianjia.com/zufang/(.+).html\"""",str(url_info))[0]
        urls.append(url_template.format(url=url))
    return urls

# 获取所有的URL
def get_urls(busi_area):
    page_amount = get_pages(busi_area)
    raw_select_url = "https://sh.lianjia.com/zufang/{busi_area}/pg{page}"
    select_url_list = list()
    urls = list()
    for i in range(1,page_amount+1):
        select_url_list.append(raw_select_url.format(busi_area=busi_area, page=i))
 
    req = CheatRequests([select_url_list])

    print([select_url_list])

    contents = req.get_cheat_all_content

    for page_text in contents:
        print(page_text)
        # a = input("DEBUG")
        # url_add = get_urls_page(page_text)
        # yield url_add

# 获取上海目录下小于100页的URL段
def get_dic_url():
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
def wirte_urls(url_add):
    with open("./output/urls.req","a+") as url:
        url.writelines(url_add)

# 将大批量的数据分批存入文件可能更可靠（？）
def create_urls(busi_area):
    for busi in busi_area:
        url_add = get_urls(busi)
        while True:
            try:
                wirte_urls(next(url_add))
            except StopIteration:
                print("迭代结束")
                break

if __name__ == "__main__":
    # 获取商圈列表 由于一般情况下不会有变化，故设为常量
    # dic_list = get_dic_url()
    # print(dic_list)

    dic_list = ['caohejing','hongkou', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu', 'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian', 'beicai', 'biyun', 'caolu', 'chuansha', 'datuanzhen', 'geqing', 'gaohang', 'gaodong', 'huamu', 'hangtou', 'huinan', 'jinqiao', 'jinyang', 'kangqiao', 'lujiazui', 'laogangzhen', 'lingangxincheng', 'lianyang', 'nichengzhen', 'nanmatou', 'sanlin', 'shibo', 'shuyuanzhen', 'tangqiao', 'tangzhen', 'waigaoqiao', 'wanxiangzhen', 'weifang', 'xuanqiao', 'xinchang', 'yuqiao1', 'yangdong', 'yuanshen', 'yangjing', 'zhangjiang', 'zhuqiao', 'zhoupu', 'chunshen', 'gumei', 'hanghua', 'huacao', 'jinhui', 'jinganxincheng', 'jinhongqiao', 'longbai', 'laominhang', 'maqiao', 'meilong', 'pujiang1', 'qibao', 'shenzhuang', 'wujing', 'zhuanqiao', 'dahua', 'dachangzhen', 'gongfu', 'gongkang', 'gucun', 'gaojing', 'jiangwanzhen', 'luojing', 'luodian', 'songbao', 'songnan', 'shangda', 'tonghe', 'yuepu', 'yanghang', 'zhangmiao']

    for dic in dic_list:
        url_adds = get_urls(dic)
        for url_add in url_adds:
            print(url_add)
            a = input("debug")

    print(url_list)