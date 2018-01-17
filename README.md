# 链家网 房源信息爬虫 （一期）

## Author Tau Woo
## Date 2018-01-17

## 实现方法
Python-BeautifulSoup + 正则匹配

## OS
Linux

## 依赖软件
```bash
# Python3 安装
sudo apt-get install python3

# BeautifulSoup 安装
sudo apt-get install python-bs4

# Python3 插件安装
pip3 install requests
pip3 install beautifulsoup4
```

## 使用方法
shell下执行 ./do_task.sh

如果需要修改爬取的页面，请修改spider\_main.py文件中的busi\_area（商圈列表）