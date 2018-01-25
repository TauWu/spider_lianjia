# -*- coding: utf-8 -*-
# spider_page 页面数据分析

import requests
from bs4 import BeautifulSoup
import re

from pprint import pprint

#TODO 后期请求附加参数将从cheat模块中获取
headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

# 具体房源： 链家整租、自如整租、自如合租
# "HouseID":房源编号
# "HouseSource":房源来源 # 1-链家整租 2-自如整租 3-自如合租
# "HouseStatus"：房源状态 # 1-在售 2-下架
# "Title": 房间详情页标题
# "HousePrice":租金
# "HouseType":户型
# "HouseArea":房间大小
# "HouseFloor":房间楼层
# "HouseOri":房间朝向
# "AddrRegion":地址行政区
# "AddrBusi":地址商圈
# "SellTime":上架时间
# "CommunityName": 地标名称
# "CommunityAddr":地标地址
# "CommunityPosi":地标坐标 - 百度坐标系
# "SeeCountSevenDay":近七天带看次数 - 链家整租有
# "SeeCount":带看总数 - 链家整租有

# "LianjiaExtra": 链家整租的其他信息
    # "HouseTypePic":户型图 - 链家整租有
# "ZiruExtra":自如整租、合租的其他信息
    # "HouseBasicInfo": 房源基础信息 - 自如合租、自如整租有
    # "HousePayInfo":房源支付信息 - 自如整租、自如合租有

# 分析链家网中房源信息总入口
def getHouseInfo(url):
    
    # 房源编号
    house_id_compile = re.compile("http://sh.lianjia.com/zufang/(.+).html")
    house_id = re.findall(house_id_compile, url)[0]
    
    # 房源来源 默认值0
    house_source = 0
    if house_id[3] != "r":
        # 链家整租
        house_source = 1

    # 获取网页基础信息
    raw_text = requests.get(url, headers=headers).text
    raw_bs = BeautifulSoup(raw_text, "lxml")

    # 房源详情页标题
    title_soup = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"title-wrapper"}).findChild("div",{"class":"content"}).findChild("div",{"class":"title"}).findChild("h1",{"class":"main"})
    title_compile = re.compile("<h1.+title=\"(.+)\".+")
    title = re.findall(title_compile,str(title_soup))[0]

    # 房源简介模块
    # 房源来源信息
    cj_cun_soup = raw_bs.findChild("div",{"class":"zf-top"}).findChild("div",{"class":"cj-cun"})
    content_soup = None

    # 上下架信息
    house_status_soup = cj_cun_soup.findChild("div",{"class":"album-box"}).findChild("div",{"class":"album-box left"}).findChild("div",{"class":"pic-panel pic-panel-hover"}).findChild("div",{"class":"tag tag_yixiajia"})

    house_status = 1

    if house_status_soup is None:
        house_status = 2

    if house_source == 1:
        content_soup = cj_cun_soup.findChild("div",{"class":"content forRent"})

    else:
        content_soup = cj_cun_soup.findChild("div",{"class":"content"})

        house_source_compile = re.compile("[\s\S]*\"houseInfo ziru_(.+)\"[\s\S]*")
        house_source_str = re.findall(house_source_compile, str(content_soup))[0]

        if house_source_str == "zhengzu":
            house_source = 2
        elif  house_source_str == "hezu":
            house_source = 3

    # 房源户型等信息解析
    basic_info = None
    if house_source == 1:
        house_info_soup = content_soup.findChild("div",{"class":"houseInfo"})
        around_info_soup = content_soup.findChild("table",{"class":"aroundInfo"}).findChildren("tr")
        basic_info = getHouseBasicInfoLJZZ(house_info_soup, around_info_soup)

    elif house_source == 2:
        house_info_soup = content_soup.findChild("div",{"class":"houseInfo ziru_zhengzu"})
        around_info_soup = content_soup.findChild("table",{"class":"aroundInfo"}).findChildren("tr")
        basic_info = getHouseBasicInfoZRZZ(house_info_soup, around_info_soup)

    elif house_source == 3:
        house_info_soup = content_soup.findChild("div",{"class":"houseInfo ziru_hezu"})
        around_info_soup = content_soup.findChild("table",{"class":"aroundInfo"}).findChildren("tr")
        basic_info = getHouseBasicInfoZRHZ(house_info_soup, around_info_soup)

    # 房源坐标信息
    posi_soup = raw_bs.findChild("div",{"class":"around js_content"})

    #TODO 此处正则待验证
    posi_lng_compile = re.compile("[\s\S]*longitude=\"(([0-9]|\.)+)\"[\s\S]*")
    posi_lat_compile = re.compile("[\s\S]*latitude=\"(([0-9]|\.)+)\"[\s\S]*")

    house_lng_posi = re.findall(posi_lng_compile, str(posi_soup))[0][0]
    house_lat_posi = re.findall(posi_lat_compile, str(posi_soup))[0][0]

    house_posi = {
        "Latitude":house_lat_posi,
        "Longitude":house_lng_posi
    }

    # 带看记录信息
    see_count = None
    see_count_seven_days = None
    if house_source == 1:
        try:
            see_soup = raw_bs.findChild("div",{"class","record js_content"}).findChild("div",{"class","panel"})

            see_count_seven_days_soup = see_soup.findChild("div", {"class":"count"})
            see_count_soup = see_soup.findChild("div",{"class","totalCount"}).findChild("span")

            see_count = re.findall("([0-9]+)",str(see_count_soup))[0]
            see_count_seven_days = re.findall("([0-9]+)",str(see_count_seven_days_soup))[0]
        
        except AttributeError:
            pass
    
    # 其他信息获取
    lianjia_extra = dict()
    ziru_extra = dict()
    if house_source != 1:
        # 获取自如的其他信息
        introduction_soup = raw_bs.findChild("div",{"id":"introduction"}).findChild("div",{"class":"introduction"}).findChild("div",{"class":"introContent"})
        # 获取基本属性
        try:
            house_basic_info_soup = introduction_soup.findChild("div",{"class":"base baseFull"}).findChild("div",{"class":"content"}).findChild("ul").findChildren("li")
            house_basic_info_compile = re.compile("([\u4e00-\u9fa5]+)")
            house_basic_info = [house_basic_info for house_basic_info in re.findall(house_basic_info_compile, str(house_basic_info_soup))][1::2]
            ziru_extra["HouseBasicInfo"] = ",".join(house_basic_info)
        except AttributeError:
            pass

        # 获取房源特色
        try:
            house_feature_infos = list()
            house_feature_info_soup = introduction_soup.findChild("div",{"class":"feature"}).find("div",{"class":"featureContent"}).findChild("ul").findChildren("li")
            house_feature_info_compile = re.compile("<span class=\"text\">([\s\S]*)</span>")
            for i in range (0, len(house_feature_info_soup)):
                house_feature_info = re.findall(house_feature_info_compile, str(house_feature_info_soup[i]))
                house_feature_infos += house_feature_info
            ziru_extra["HouseFeatureInfo"] = house_feature_infos
        except AttributeError:
            pass

        # 获取支付方式
        try:
            payment_list = list()
            payment_soup = raw_bs.findChild("div",{"class":"payment js_content"}).findChild("div",{"class":"content"}).findChild("table",{"class":"paylist"}).findChildren("tr")
            payment_compile = re.compile("<tr.+<td>(.+)</td><td>(.+)</td><td>(.+)</td><td>(.+)</td>.+</tr>")
            for i in range(1, len(payment_soup)):
                payment = list(re.findall(payment_compile, str(payment_soup[i]).strip().replace('\n',''))[0])
                payment = {"方式":payment[0],"租金":payment[1],"押金":payment[2],"服务费":payment[3]}
                payment_list.append(payment)
            ziru_extra["PaymentList"] = payment_list

        except AttributeError:
            pass

    else:
        # 链家其他信息获取
        try:
            house_type_pic_soup = raw_bs.findChild("div",{"class":"content-wrapper huxing js_content"}).findChild("div",{"class":"container"}).findChild("div",{"class":"hx_pic"}).findChild("a")

            house_type_pic_compile = re.compile(".+href=\"(.+)\" target=.+")
            house_type_pic = re.findall(house_type_pic_compile, str(house_type_pic_soup))[0]
            lianjia_extra["HouseTypePic"] = house_type_pic
        except AttributeError:
            pass

    # print(house_id, title, house_source, basic_info, house_posi, see_count, see_count_seven_days, ziru_extra, lianjia_extra)

    return {
        "HouseID":house_id,
        "HouseSource":house_source,
        "HouseStatus":house_status,
        "Title":title,
        "HousePrice":basic_info[0],
        "HouseType":basic_info[1],
        "HouseArea":basic_info[2],
        "HouseFloor":basic_info[3],
        "HouseOri":basic_info[4],
        "AddrRegion":basic_info[5],
        "AddrBusi":basic_info[6],
        "SellTime":basic_info[7],
        "CommunityName":basic_info[8],
        "CommunityAddr":basic_info[9],
        "CommunityPosi":house_posi,
        "SeeCountSevenDay":see_count_seven_days,
        "SeeCount":see_count,
        "ZiruExtra":ziru_extra,
        "LianjiaExtra":lianjia_extra
    }

def getHouseBasicInfoLJZZ(house_info_soup, around_info_soup):

    # 租金
    house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info_soup.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))[0]

    # 房型
    house_type = re.findall("""<div class="mainInfo">(.+)<span class="unit">室</span>.([0-9])<span class="unit">厅</span></div>""",str(house_info_soup.findChild("div",{"class":"room"}).findChild("div",{"class":"mainInfo"})))[0]
    house_type = "%s室%s厅"%(house_type[0],house_type[1])

    # 房间面积
    house_area = re.findall("""<div class="mainInfo">(.+)<span class="unit">平</span></div>""",str(house_info_soup.findChild("div",{"class":"area"}).findChild("div",{"class":"mainInfo"})))
    house_area = "%s平"%(house_area[0])

    # 解析第一行数据
    tb1 = around_info_soup[0].findChildren("td",{"width":"50%"})
    house_floor = re.findall("""<td width="50%">(.+)</td>""", str(tb1[0]))[0]
    house_ori = str(re.findall("""<td width="50%">([\s\S]*)</td>""", str(tb1[1]))).replace(" ","").replace("\\n","").replace("\\t","")[2:-2]

    # 解析第二行数据
    tb2 = around_info_soup[1].findChildren("td",{"width":"50%"})
    house_location = re.findall("""<td width="50%"><a href=".+" target="_blank">(.+)</a> <a href=".+" target="_blank">(.+)</a></td>""", str(tb2))[0]
    addr_region = house_location[0]
    addr_busi = house_location[1]
    sell_time = re.findall("""<td width="50%">(.+)</td>""", str(tb2[1]))
    if len(sell_time) != 0:
        sell_time = sell_time[0]
    else:
        sell_time = None

    # 解析第三行数据
    tb3 = around_info_soup[2].findChild("p",{"class","addrEllipsis"})
    community_name = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb3))[0]

    # 解析第四行数据
    tb4 = around_info_soup[3].findChild("p",{"class","addrEllipsis"})
    community_addr = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb4))[0].replace(",","，")

    return house_price, house_type, house_area, house_floor, house_ori, addr_region, addr_busi, sell_time, community_name, community_addr

def getHouseBasicInfoZRZZ(house_info_soup, around_info_soup):
    return getHouseBasicInfoLJZZ(house_info_soup, around_info_soup)

def getHouseBasicInfoZRHZ(house_info_soup, around_info_soup):
    # 房间价格
    house_price = re.findall("""<div class="mainInfo bold" style="font-size:28px;">(.+)<span.+</div>""",str(house_info_soup.findChild("div",{"class":"price"}).findChild("div",{"class":"mainInfo bold"})))[0]

    # 房间面积
    house_area = re.findall("""<div class="mainInfo">(.+)<span class="unit">平</span></div>""",str(house_info_soup.findChild("div",{"class":"area"}).findChild("div",{"class":"mainInfo"})))
    house_area = "%s平"%(house_area[0])

    # 解析第一行数据
    tb1 = around_info_soup[0].findChildren("td",{"width":"50%"})
    house_type = re.findall("""<td width="50%">(.+)</td>""", str(tb1[0]))[0]
    house_area =re.findall("""<td width="50%">(.+)</td>""", str(tb1[1]))[0]

    # 解析第二行数据
    tb2 = around_info_soup[1].findChildren("td",{"width":"50%"})
    house_floor = re.findall("""<td width="50%">(.+)</td>""", str(tb2[0]))[0]
    house_ori = str(re.findall("""<td width="50%">([\s\S]*)</td>""", str(tb2[1]))).replace(" ","").replace("\\n","").replace("\\t","")[2:-2]

    # 解析第三行数据
    tb3 = around_info_soup[2].findChildren("td",{"width":"50%"})
    house_location = re.findall("""<td width="50%"><a href=".+" target="_blank">(.+)</a> <a href=".+" target="_blank">(.+)</a></td>""", str(tb3))[0]
    addr_region = house_location[0]
    addr_busi = house_location[1]
    sell_time = re.findall("""<td width="50%">(.+)</td>""", str(tb3[1]))
    sell_time = re.findall("""<td width="50%">(.+)</td>""", str(tb2[1]))
    if len(sell_time) != 0:
        sell_time = sell_time[0]
    else:
        sell_time = None

    # 解析第三行数据
    tb4 = around_info_soup[3].findChild("p",{"class","addrEllipsis"})
    community_name = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb4))[0]

    # 解析第四行数据
    tb5 = around_info_soup[4].findChild("p",{"class","addrEllipsis"})
    community_addr = re.findall("""<p class="addrEllipsis" title="(.+)">[\s\S]*""", str(tb5))[0].replace(",","，")

    return house_price, house_type, house_area, house_floor, house_ori, addr_region, addr_busi, sell_time, community_name, community_addr

if __name__ == "__main__":
    urls = [
        "http://sh.lianjia.com/zufang/shz4277432.html",
        "http://sh.lianjia.com/zufang/shz4277132.html",
        "http://sh.lianjia.com/zufang/shzr100000000.html",
        "http://sh.lianjia.com/zufang/shzr100043293.html",
        "http://sh.lianjia.com/zufang/shz4301605.html"
    ]

    for url in urls:
        pprint(getHouseInfo(url))
        print("\n")
