#!/bin/bash

# 安装 Python3
sudo apt-get install python3

# 安装 Python-Pip
sudo apt-get install python3-pip

# 安装 BeautifulSoup
sudo apt-get install python-bs4

# 安装 Git
sudo apt-get install git

# 安装Redis
sudo apt-get install redis-server

# 安装依赖库
pip3 install requests
pip3 install beautifulsoup4
pip3 install PyMySQL
pip3 install fake-useragent
pip3 install gevent
pip3 install lxml
sudo pip3 install redis

# Clone项目
mkdir /data/
mkdir /data/code/
sudo chmod -R 777 /data/code/
cd /data/code/
git clone git@github.com:TauWu/spider_lianjia.git

# 测试代理
cd /data/code/spider_lianjia/
python3 spider_main.py test1

# MySQL配置
sudo apt-get install mysql-server
sudo apt-get install mysql-client

mysql -u root -p < /data/code/spider_lianjia/database/create_database.sql

# 测试爬虫代码
cd /data/code/spider_lianjia/
python3 install_operator.py
python3 spider_main.py spider