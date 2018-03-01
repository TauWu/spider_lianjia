#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from module.database import DBController
from util.common.date import Time
import sys

from util.common.logger import use_logger

@use_logger(level="info")
def db_optor_info(msg):
    pass

# 这里存放可能会有操作的SQL语句模板
house_info_name = "lianjia_house_info"
house_stat_name = "lianjia_house_stat_json"
welcome_str = """
请输入您需要进行的操作的数字编号：
---
[0] 退出。
[1] 备份当前数据表为当前时间，并创建新的空数据表。
[2] 清空当前数据表。
[3] 新建数据表。

---

"""

truncate_sql = "truncate table `{tablename}`"
rename_sql = "rename table `{fromname}` to `{toname}`"

create_house_info_table = """
        CREATE TABLE IF NOT EXISTS `{tablename}` (
        `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
        `house_id` varchar(15) NOT NULL COMMENT '房源编号',
        `house_title` varchar(63) NOT NULL COMMENT '房源标题' DEFAULT '',
        `insert_date` varchar(15) NOT NULL COMMENT '入库日期' DEFAULT '',
        `district` varchar(31) NOT NULL COMMENT '行政区' DEFAULT '',
        `community_id` varchar(31) NOT NULL COMMENT '地标ID' DEFAULT '',
        `community_name` varchar(31) NOT NULL COMMENT '地标名称' DEFAULT '',
        `house_type` varchar(8) NOT NULL COMMENT '房型' DEFAULT '',
        `house_type_new` varchar(31) NOT NULL COMMENT '房型（详情页面）' DEFAULT '',
        `house_area` varchar(8) NOT NULL COMMENT '面积大小' DEFAULT '',
        `orientation` varchar(8) NOT NULL COMMENT '朝向' DEFAULT '',
        `distinct_name` varchar(31) NOT NULL COMMENT '行政区名称' DEFAULT '',
        `house_floor` varchar(8) NOT NULL COMMENT '房间楼层' DEFAULT '',
        `house_total_floor` varchar(8) NOT NULL COMMENT '总楼层' DEFAULT '',
        `house_create_year` varchar(31) NOT NULL COMMENT '建房时间' DEFAULT '',
        `see_count` int(4) NOT NULL COMMENT '带看人数' DEFAULT 0,
        `house_price` int(6) NOT NULL COMMENT '房间价格' DEFAULT 0,
        `sale_date` varchar(15) NOT NULL COMMENT '上架时间' DEFAULT '1999-12-31',
        `sale_date_new` varchar(31) NOT NULL COMMENT '上架时间（详情页面）' DEFAULT '-1天前发布',
        `extra_info_select` varchar(511) NOT NULL COMMENT '房间标签' DEFAULT '',
        `basic_info` varchar(63) NOT NULL COMMENT '基本属性' DEFAULT '',
        `house_tags` varchar(63) COMMENT '房源标签' DEFAULT '',
        `house_feature` varchar(1023) COMMENT '房源特色' DEFAULT '',
        `position` varchar(31) COMMENT '房源坐标' DEFAULT '0,0',
        `see_stat_total` int(4) COMMENT '带看总数' DEFAULT 0,
        `see_stat_weekly` int(4) COMMENT '周带看总数' DEFAULT 0,
        `community_sold_count` int(4) COMMENT '同小区成交数' DEFAULT 0,
        `busi_sold_count` int(4) COMMENT '同商圈成交数' DEFAULT 0,
        
        `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
        `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        UNIQUE KEY `house_id` (`house_id`, `insert_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""

create_house_stat_table = """

        CREATE TABLE IF NOT EXISTS `{tablename}` (
        `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
        `house_id` varchar(15) NOT NULL COMMENT '房源编号',
        `insert_date` varchar(15) NOT NULL COMMENT '入库日期' DEFAULT '',
        `house_stat_json` text COMMENT '房源统计json',

        `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
        `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        UNIQUE KEY `house_id` (`house_id`, `insert_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""

def create(db):
    '''新建空表操作'''
    c1_sql = create_house_info_table.format(tablename=house_info_name)
    c2_sql = create_house_stat_table.format(tablename=house_stat_name)

    db.execute(c1_sql)
    db.execute(c2_sql)


def truncate(db):
    '''清空缓存表操作'''
    t1_sql = truncate_sql.format(tablename=house_info_name)
    t2_sql = truncate_sql.format(tablename=house_stat_name)

    db.execute(t1_sql)
    db.execute(t2_sql)

def backup_table(db, t):
    '''备份缓存表操作'''
    b1_sql = rename_sql.format(fromname=house_info_name,toname="%s_%s"%(house_info_name, t))
    b2_sql = rename_sql.format(fromname=house_stat_name,toname="%s_%s"%(house_stat_name, t))

    db.execute(b1_sql)
    db.execute(b2_sql)

    create(db)

if __name__ == "__main__":
    # 创建数据库连接
    db = DBController()
    
    # 获取当前时间
    t = Time.now_datetime_str()

    # 不携带参数的情况下交互式数据库操作
    if len(sys.argv) == 1:

        while True:

            opeartor = input(welcome_str)

            if opeartor.strip() == "0":
                db_optor_info("程序退出...")
                break

            elif opeartor.strip() == "1":
                db_optor_info("开始备份数据表...")
                backup_table(db, t)
                db_optor_info("备份完成！")

            elif opeartor.strip() == "2":
                db_optor_info("开始清空该数据表...")
                truncate(db)
                db_optor_info("清空完成！")

            elif opeartor.strip() == "3":
                db_optor_info("开始创建新的数据表...")
                create(db)
                db_optor_info("创建完成！")

            else:
                db_optor_info("\n【%s】操作不存在，请重新选择！"%opeartor)
                continue

    # 携带一个参数的情况下直接执行一次该操作 - 为定时任务开发
    elif len(sys.argv) == 2:

        opeartor = sys.argv[1]

        if opeartor.strip() == "1":
            db_optor_info("开始备份数据表...")
            backup_table(db, t)
            db_optor_info("备份完成！")

        elif opeartor.strip() == "2":
            db_optor_info("开始清空该数据表...")
            truncate(db)
            db_optor_info("清空完成！")

        elif opeartor.strip() == "3":
            db_optor_info("开始创建新的数据表...")
            create(db)
            db_optor_info("创建完成！")
    
    else:
        raise ValueError("参数太多")

    db.close