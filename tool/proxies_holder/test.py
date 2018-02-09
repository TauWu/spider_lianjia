import requests
import json
import re
import time

from proxies import IPDBController

db = IPDBController()

proxie = {}

while True:
    proxies_get = json.loads(requests.get("http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=e03d2d5a04bc4a9ead944036f1d72c48&orderno=MF20181310506Pzv7b3&returnType=2&count=10").text)["RESULT"]
    print(proxies_get)
    for proxies in proxies_get:
        proxie["http"] = "http://{ip}:{port}".format(ip=proxies["ip"], port=proxies["port"])
        try:
            req = requests.get("http://2017.ip138.com/ic.asp",proxies=proxie)
            print(re.findall(r"<center>您的IP是：\[(.+)\] 来自：(.+)</center>",req.content.decode("gb2312")))
            db.insert_ip([[proxies["ip"],proxies["port"],"HTTP"]])
        except Exception:
            pass
    time.sleep(5)


