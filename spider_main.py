# -*- coding:utf-8 -*-

from select_url import get_urls
from spider_page import getHouseInfo
from spider_page import getHouseInfoOther
import time

busi_area = ["caohejing","wujiaochang"]

# 通过文件来中转 监控程序运行情况
def create_task(busi_area):
    urls = list()
    for busi in busi_area:
        urls += get_urls(busi)
    with open("urls.req","w") as f:
        f.writelines(urls)

# 读取文件内部URL以发起请求
def do_task():
    with open("result.csv","a+") as result:
        result.write("编号,价格,户型,面积,楼层,朝向,行政区,商圈,上线日期,地标名称,地标地址\n")
    with open("urls.req","r") as f:
        urls = f.readlines()
        if len(urls) != 0:
            for url in urls:
                try:
                    info = getHouseInfo(url[:-1])
                    with open("result.csv","a+") as result:
                        result.write(info)
                except AttributeError:
                    try:
                        info = getHouseInfoOther(url[:-1])
                        with open("result.csv","a+") as result:
                            result.write(info)
                    except AttributeError:
                        with open("errs.req","a+") as err:
                            err.write(url)
                finally:
                    time.sleep(0.3)

        else:
            print("urls.req文件为空，请检查")

if __name__ == "__main__":
    create_task(busi_area)
    do_task()