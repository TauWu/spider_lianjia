# SHELL

## 命令行程序
- 主要存放可能调用到的方法、工具的shell文件

### SHELL目录文件介绍
文件名称 | 文件功能 | 主要命令
--- | --- | ---
spider_start_all.sh | 开始爬取所有的房源信息 | python3 spider_main.py all
spider\_start.sh | 开始爬取task\.csv指定商圈的上线房源信息 | python3 spider\_main.py
clean_output.sh | 自动清理程序运行过程中的输出文件 | 输出重定向
install.sh | 安装所需要的软件、依赖库等 | - 