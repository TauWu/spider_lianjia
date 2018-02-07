CREATE TABLE `lianjia_house_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `house_id` varchar(15) NOT NULL COMMENT '房源编号',
  `house_title` varchar(63) NOT NULL COMMENT '房源标题' DEFAULT '',
  `community_id` varchar(15) NOT NULL COMMENT '地标ID' DEFAULT '',
  `community_name` varchar(31) NOT NULL COMMENT '地标名称' DEFAULT '',
  `house_type` varchar(8) NOT NULL COMMENT '房型' DEFAULT '',
  `house_area` varchar(8) NOT NULL COMMENT '面积大小' DEFAULT '',
  `orientation` varchar(8) NOT NULL COMMENT '朝向' DEFAULT '',
  `distinct_name` varchar(31) NOT NULL COMMENT '行政区名称' DEFAULT '',
  `house_floor` varchar(8) NOT NULL COMMENT '房间楼层' DEFAULT '',
  `house_create_year` varchar(31) NOT NULL COMMENT '建房时间' DEFAULT '',
  `see_count` int(4) NOT NULL COMMENT '带看人数' DEFAULT 0,
  `house_price` int(6) NOT NULL COMMENT '房间价格' DEFAULT 0,
  `sale_date` varchar(15) NOT NULL COMMENT '上架时间' DEFAULT '1999-12-31',
  `extra_info_select` varchar(511) NOT NULL COMMENT '房间标签' DEFAULT '',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;