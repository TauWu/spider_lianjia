-- 空服务器建表语句 只执行一次

CREATE DATABASE IF NOT EXISTS `spider_data`;

USE `spider_data`;

CREATE TABLE IF NOT EXISTS `lianjia_house_info` (
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


CREATE TABLE IF NOT EXISTS `lianjia_house_stat_json` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `house_id` varchar(15) NOT NULL COMMENT '房源编号',
  `insert_date` varchar(15) NOT NULL COMMENT '入库日期' DEFAULT '',
  `house_stat_json` text COMMENT '房源统计json',

  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `house_id` (`house_id`, `insert_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;