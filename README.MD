# SPIDER_LIANJIA

## 基础信息
Author | CreateDate | ProjectName | ChineseName
--- | --- | --- | ---
Tau Woo | 2018-01-17 | spider_name | 链家网 房源信息爬虫（一期）

## 实现方法
+ 1 使用requests读取网页
>+ 1.1 使用requests代理和使用不同的User-Agent来欺骗被爬取的服务器
+ 2 使用BeautifulSoup（lxml）层层解析网页
+ 3 使用正则匹配获取想要取用的数据字段
+ 4 将获取的数据输出到csv文件/保存到数据库

## OS
Linux Deepin-15.5 (Debian 6.3.0-11)

## 软件依赖
```bash
# Python3 安装
sudo apt-get install python3

# BeautifulSoup 安装
sudo apt-get install python-bs4

# Python3 插件安装
pip3 install requests
pip3 install beautifulsoup4

# 数据库连接模块
pip3 install PyMySQL

########## 以下为伪造请求需要的库 ##########
# 以下为使用socket5代理需要安装，其中PySocks可能会在上一个命令中自动安装
pip3 install requests\[socks\]
pip3 install PySocks

# 伪造UA安装库
pip3 install fake-useragent

```

## 使用方法
+ 执行shell目录下对应的不同的shell文件可以执行不同的功能
>+ 可以参考spider_main.py中的__main__函数判断不同的调用方法的结果
>+ 直接执行spider_main.py会先读取当前目录的task.csv文件的商圈名称，`请先在网页端确定该商圈存在并且拼音无误`，否则将会爬取全量数据，时间消耗会比较大