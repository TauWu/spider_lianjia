#!/bin/bash

# 安装 Python3
sudo apt-get install python3

# 安装 Python-Pip
sudo apt-get install python3-pip

# 安装 BeautifulSoup
sudo apt-get install python-bs4

# 安装 Git
sudo apt-get install git

# 安装依赖库
pip3 install requests
pip3 install beautifulsoup4
pip3 install PyMySQL
pip3 install fake-useragent
pip3 install gevent
pip3 install lxml

# Clone项目
mkdir /data/
mkdir /data/code/
mkdir /data/code/yujian/
sudo chmod -R 777 /data/code/
cd /data/code/yujian/
git clone git@github.com:TauWu/spider_lianjia.git

# 测试代理
cd /data/code/yujian/spider_lianjia/
python3 spider_main.py test1