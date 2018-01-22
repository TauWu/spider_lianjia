# OUTPUT

## 本目录下文件介绍
文件名称 | 文件生成模块 | 文件作用
--- | --- | ---
./urls.req | module.spider.select_url | 保存查询房源列表可以获取的`所有房源详情URL`
./result.csv | module.spider.spider_page | 保存解析房源详情列表获得的所有`房源信息`的csv信息，一般作为本程序运行的结果
./errs.req | spider_main | 主程序在爬取房源详情页面失败时，保存`不能用当前模块解析的错误URL`