# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from spider_page import headers
import re

# 获取该搜索条件下拥有的房间数目
def get_pages(busi_area):
    raw_url = "http://sh.lianjia.com/zufang/{busi_area}"
    raw_text = requests.get(raw_url.format(busi_area=busi_area),headers=headers).text
    bs4 = BeautifulSoup(raw_text,"lxml")

    totalAmount = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-head clear"}).findChild("h2").findChild("span")
    page_amount = int(int(re.findall("<span>(.+)</span>", str(totalAmount))[0])/20) + 1
    
    return page_amount

# 获取筛选页面的所有房间URL
def get_urls_page(select_url):
    url_template = "http://sh.lianjia.com{url}.html\n"
    page_text = requests.get(select_url, headers=headers).text
    bs4 = BeautifulSoup(page_text, "lxml")
    urls = list()
    room_list = bs4.findChild("div",{"class":"main-box clear"}).findChild("div",{"class":"con-box"}).findChild("div",{"class":"list-wrap"}).findChild("ul",{"class","house-lst js_fang_list"}).findChildren("li")
    for room_info in room_list:
        url_info = room_info.findChild("div",{"class","info-panel"}).findChild("h2").findChild("a",{"class":"js_triggerGray js_fanglist_title"})
        url = re.findall(""".+href=\"(.+).html\"""",str(url_info))[0]
        urls.append(url_template.format(url=url))
    return urls

# 获取所有的URL
def get_urls(busi_area):
    page_amount = get_pages(busi_area)
    raw_select_url = "http://sh.lianjia.com/zufang/{busi_area}/d{page}"
    urls = list()
    for i in range(1,page_amount+1):
        select_url = raw_select_url.format(busi_area=busi_area, page=i)
        urls += get_urls_page(select_url)
    return urls

if __name__ == "__main__":
    print(get_urls("caohejing"))