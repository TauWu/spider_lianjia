# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}


def getHouseInfo(url):
    # 获取网页基础信息
    raw_text = requests.get(url, headers=headers).text
    raw_bs = BeautifulSoup(raw_text)
    rent_info = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"cj-cun"}).findChild("div",{"class","content forRent"})
    house_info = rent_info.findChild("div",{"class":"houseInfo"})
    around_info = rent_info.findChild("table",{"class":"aroundInfo"}).findChildren("tr")


    # 获取实际需要爬取的信息
    # 房间价格
    house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))
    house_price = "%s元/月,"%(house_price[0])
    # 房间信息（几室几厅）
    room_info = re.findall("""<div class="mainInfo">(.+)<span class="unit">室</span>(.+)<span class="unit">厅</span></div>""",str(house_info.findChild("div",{"class":"room"}).findChild("div",{"class":"mainInfo"})))
    room_info = "%s室%s厅,"%(room_info[0][0],room_info[0][1])
    # 房间面积
    room_area = re.findall("""<div class="mainInfo">(.+)<span class="unit">平</span></div>""",str(house_info.findChild("div",{"class":"area"}).findChild("div",{"class":"mainInfo"})))
    room_area = "%s平,"%(room_area[0])

    # 解析第一行数据
    tb1 = around_info[0].findChildren("td",{"width":"50%"})
    room_floor = re.findall("""<td width="50%">(.+)</td>""", str(tb1[0]))[0]
    room_ori = str(re.findall("""<td width="50%">([\s\S]*)</td>""", str(tb1[1]))).replace(" ","").replace("\\n","").replace("\\t","")[2:-2]

    # 解析第二行数据
    tb2 = around_info[1].findChildren("td",{"width":"50%"})
    room_location = re.findall("""<td width="50%"><a href=".+" target="_blank">(.+)</a> <a href=".+" target="_blank">(.+)</a></td>""", str(tb2))
    sell_time = re.findall("""<td width="50%">(.+)</td>""", str(tb2[1]))[0]

    # 解析第三行数据
    tb3 = around_info[2].findChild("p",{"class","addrEllipsis"})
    community_name = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb3))[0]

    # 解析第四行数据
    tb4 = around_info[3].findChild("p",{"class","addrEllipsis"})
    community_addr = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb4))[0]


    return {"HousePrice" :house_price,
    "RoomInfo" :room_info,
    "RoomArea" :room_area,
    "RoomFloor":room_floor,
    "RoomOri": room_ori,
    "RoomLocation":room_location,
    "SellTime": sell_time,
    "CommunityName": community_name,
    "CommunityAddr": community_addr}

if __name__ == "__main__":
    print(getHouseInfo("http://sh.lianjia.com/zufang/shz4223367.html"))
