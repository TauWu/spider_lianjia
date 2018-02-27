# SPIDER_LIANJIA

## 基础信息
Author | CreateDate | ProjectName | ChineseName
--- | --- | --- | ---
Tau Woo | 2018-01-17 | spider_lianjia | 链家网 租房房源信息爬虫（一期）

## 实现方法
+ 1 使用requests读取网页、获取Api返回数据
>+ 1.1 使用端口转发修改请求IP和使用不同的User-Agent来欺骗被爬取的服务器
+ 2 使用BeautifulSoup（lxml）解析网页
+ 3 使用正则匹配获取想要取用的数据字段
+ 4 将获取的数据保存到数据库，并依赖数据库的UNIQUE KEY的唯一性来保证某一日数据的唯一性

## OS
Linux Deepin-15.5 (Debian 6.3.0-11)

## 软件依赖
```bash
# 安装 Python3 和 pip
sudo apt-get install python3
sudo apt-get install python3-pip

# 安装 BeautifulSoup
sudo apt-get install python-bs4

# 安装依赖库
pip3 install requests
pip3 install beautifulsoup4
pip3 install lxml
pip3 install PyMySQL
pip3 install gevent
pip3 install fake-useragent

########## 以下为可选安装库 ##########
# 以下为使用socket5代理需要安装，其中PySocks可能会在上一个命令中自动安装
pip3 install requests\[socks\]
pip3 install PySocks

```

## 并发（分布式）爬虫的建议

### 可拆解部分
#### 1. 商圈拆解
#### 2. 爬虫步骤拆解（数据写入拆解）

### 建议
- 定时任务每日执行全量数据爬取
- 执行任务前需要将昨天的数据表重命名并新建一张表
- 每台机器可以跑几个商圈
- 每台机器可以分开跑不同步骤
- 代码中已经用协程提高并发量，不建议再开多进程

## 使用方法

### 执行python3 spider_main.py并携带参数

#### 操作参数有三种，分别对应不同的操作： 
- **create** - 爬虫第一步：爬取筛选页面，筛选条件是页数小于100的地标
- **page** - 爬虫第二步：爬取详情页面，从数据库头遍历
- **stat** - 爬虫第三步：爬取内置统计接口，从数据库头遍历

#### 具体操作案例说明：
编号 | 命令 | 说明
--- | --- | ---
1| python3 spider_main.py |读取程序根目录下task.csv文件中的商圈名称，并依次执行第1、2、3步。
2| python3 spider_main.py create | 从task.csv文件中获取待爬取商圈，同时执行爬虫第一步（写入lianjia\_house\_info表中）
3| python3 spider_main.py page | 从lianjia\_house\_info表中第一个开始往后以某一固定步长请求房源详情页面，更新第一步未获取到的字段
4| python3 spider_main.py stat | 从lianjia\_house\_info表中第一个开始往后以某一固定步长请求房源销售接口，更新第一步未获取到的字段
5| python3 spider_main.py all | 爬取所有商圈的所有房源，并且执行所有步骤（约9小时）
6| python3 spider_main.py all1 | 先获取所有商圈的列表 后爬取所有商圈的所有房源，并且执行所有步骤（约9小时）
7| python3 spider_main.py create [argv1] | 从参数中获取待爬取商圈，同时执行爬虫第一步（写入lianjia\_house\_info表中）
8| python3 spider_main.py page [argv1] | 从参数中获取并发量，同时执行爬虫第二步（写入lianjia\_house\_info表中）
9| python3 spider_main.py stat [argv1] | 从参数中获取并发量，同时执行爬虫第三步（写入lianjia\_house\_info表中）
10| python3 spider_main.py spider [argv1] | 从参数中获取待爬取商圈，同时执行爬虫第1、2、3步（写入lianjia\_house\_info表中）