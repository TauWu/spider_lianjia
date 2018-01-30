# CHEAT_MODULE

## 服务端欺骗模块
- 1.使用IP代理服务欺骗被爬取服务
- 2.使用随机UA欺骗被爬取服务

## 示例代码
### 1.普通的HTTP代理
```py
import requests

proxies = {
    "http":"http://10.10.10.100:1080",
    "https":"http://10.10.10.100:1081"
}
raw_req = requests.get("http://example.com", proxies=proxies)
```
### 2. socks v5代理
> socks功能为requests 2.10.0的新功能，使用之前需要确认requests库版本
#### 需要额外的依赖
```sh
# shell中执行使用\转义中括号
pip3 install requests\[socks\]
# PySocks可能会在上一个命令中自动安装
pip3 install PySocks

```
#### 示例代码
```py
import requests
import socks
import socket

proxies = {
    "http":"socks5://127.0.0.1:1080",
    "https":"socks5://127.0.0.1:1080"
}
raw_req = requests.get("http://example.com",proxies=proxies)
```
#### 可以测试IP地址的API
> [IP138](http://2017.ip138.com/ic.asp)
> [ChinaZ](http://ip.chinaz.com/getip.aspx)