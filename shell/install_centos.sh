#!/bin/bash

# 安装 Python3
cd ~
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz
tar Jxvf Python-3.5.0.tar.xz
cd Python-3.5.0
./configure --prefix=/usr/local/python3
make && make install
ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

# 安装 BeautifulSoup
yum install python-bs4

# 安装 Git
yum install git

# 安装Redis
yum install redis

# 安装依赖库
pip3 install --upgrade pip
pip3 install requests
pip3 install beautifulsoup4
pip3 install PyMySQL
pip3 install fake-useragent
pip3 install gevent
pip3 install lxml
pip3 install redis

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
chmod -R 777 /data/code/
cd /data/code/yujian/
git clone git@github.com:TauWu/spider_lianjia.git

# 测试代理
cd /data/code/yujian/spider_lianjia/
python3 spider_main.py test1

# MySQL配置
yum install mysql-server
yum install mysql-client

mysql -u root -p < /data/code/yujian/spider_lianjia/database/create_database.sql

# 测试爬虫代码
cd /data/code/yujian/spider_lianjia/
python3 install_operator.py
python3 spider_main.py spider