# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}


def getHouseInfo(url):

    house_id = re.findall("http://sh.lianjia.com/zufang/(.+).html",url)[0]

    # 获取网页基础信息
    raw_text = requests.get(url, headers=headers).text
    raw_bs = BeautifulSoup(raw_text,"lxml")
    rent_info = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"cj-cun"}).findChild("div",{"class","content forRent"})
    if rent_info is None: # 针对特殊的自如整租所做的防御
        rent_info = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"cj-cun"}).findChild("div",{"class","content"})
    house_info = rent_info.findChild("div",{"class":"houseInfo"})
    house_price = None
    if house_info is None: # 针对特殊的自如整租所做的防御
        house_info = rent_info.findChild("div",{"class":"houseInfo ziru_zhengzu"})
        house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))
        house_price = "%s元/月(季付)"%(house_price[0])
    around_info = rent_info.findChild("table",{"class":"aroundInfo"}).findChildren("tr")


    # 获取实际需要爬取的信息
    # 房间价格
    if house_price is None:
        house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))
        house_price = "%s元/月"%(house_price[0])
    # 房间信息（几室几厅）
    room_info = re.findall("""<div class="mainInfo">(.+)<span class="unit">室</span>.([0-9])<span class="unit">厅</span></div>""",str(house_info.findChild("div",{"class":"room"}).findChild("div",{"class":"mainInfo"})))
    room_info = "%s室%s厅"%(room_info[0][0],room_info[0][1])
    # 房间面积
    room_area = re.findall("""<div class="mainInfo">(.+)<span class="unit">平</span></div>""",str(house_info.findChild("div",{"class":"area"}).findChild("div",{"class":"mainInfo"})))
    room_area = "%s平"%(room_area[0])

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
    community_addr = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb4))[0].replace(",","，")


    # return {"HousePrice" :house_price,
    # "RoomInfo" :room_info,
    # "RoomArea" :room_area,
    # "RoomFloor":room_floor,
    # "RoomOri": room_ori,
    # "RoomLocation":room_location,
    # "SellTime": sell_time,
    # "CommunityName": community_name,
    # "CommunityAddr": community_addr}
    return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(house_id,house_price,room_info,room_area,room_floor,room_ori,room_location[0][0],room_location[0][1],sell_time,community_name,community_addr)

# 根据实际操作，有一部分URL打开的页面不同于之前的样式，需要重新读取
def getHouseInfoOther(url):

    house_id = re.findall("http://sh.lianjia.com/zufang/(.+).html",url)[0]

    # 获取网页基础信息
    raw_text = requests.get(url, headers=headers).text
    raw_bs = BeautifulSoup(raw_text,"lxml")
    content = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"cj-cun"}).findChild("div",{"class","content"})
    
    house_info = content.findChild("div",{"class":"houseInfo ziru_hezu"})
    around_info = content.findChild("table",{"class":"aroundInfo"}).findChildren("tr")

    # 获取实际需要爬取的信息
    # 房间价格
    house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))
    house_price = "%s元/月(季付)"%(house_price[0])
    # 房间面积
    room_area = re.findall("""<div class="mainInfo">(.+)<span class="unit">平</span></div>""",str(house_info.findChild("div",{"class":"area"}).findChild("div",{"class":"mainInfo"})))
    room_area = "%s平"%(room_area[0])

    # 解析第一行数据
    tb1 = around_info[0].findChildren("td",{"width":"50%"})
    room_info = re.findall("""<td width="50%">(.+)</td>""", str(tb1[0]))[0]
    house_area =re.findall("""<td width="50%">(.+)</td>""", str(tb1[1]))[0]

    # 解析第二行数据
    tb2 = around_info[1].findChildren("td",{"width":"50%"})
    room_floor = re.findall("""<td width="50%">(.+)</td>""", str(tb2[0]))[0]
    room_ori = str(re.findall("""<td width="50%">([\s\S]*)</td>""", str(tb2[1]))).replace(" ","").replace("\\n","").replace("\\t","")[2:-2]

    # 解析第三行数据
    tb3 = around_info[2].findChildren("td",{"width":"50%"})
    room_location = re.findall("""<td width="50%"><a href=".+" target="_blank">(.+)</a> <a href=".+" target="_blank">(.+)</a></td>""", str(tb3))
    sell_time = re.findall("""<td width="50%">(.+)</td>""", str(tb3[1]))[0]

    # 解析第三行数据
    tb4 = around_info[3].findChild("p",{"class","addrEllipsis"})
    community_name = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb4))[0]

    # 解析第四行数据
    tb5 = around_info[4].findChild("p",{"class","addrEllipsis"})
    community_addr = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb5))[0].replace(",","，")


    # return {"HousePrice" :house_price,
    # "RoomInfo" :room_info,
    # "RoomArea" :room_area,
    # "RoomFloor":room_floor,
    # "RoomOri": room_ori,
    # "RoomLocation":room_location,
    # "SellTime": sell_time,
    # "CommunityName": community_name,
    # "CommunityAddr": community_addr}
    return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(house_id,house_price,room_info,room_area,room_floor,room_ori,room_location[0][0],room_location[0][1],sell_time,community_name,community_addr)



if __name__ == "__main__":
    print(getHouseInfo("http://sh.lianjia.com/zufang/shz4412899.html"))
