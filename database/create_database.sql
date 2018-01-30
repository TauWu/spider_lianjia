
CREATE TABLE `lianjia_house_info_json` (
  `house_id` varchar(30) NOT NULL COMMENT '房源编号',
  `house_info` varchar(1023) DEFAULT NULL COMMENT '房源信息',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`house_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `proxies_pool` (
  `ip` varchar(20) NOT NULL COMMENT 'IP',
  `port` varchar(8) NOT NULL COMMENT '端口号',
  `type` varchar(8) NOT NULL COMMENT '代理类型',
  `extra` varchar(256) DEFAULT NULL COMMENT '附加信息',
  `failed` int(11) NOT NULL DEFAULT '0' COMMENT '失败次数（删除失败超过五次的代理）',
  `deleted` int(11) NOT NULL DEFAULT '0' COMMENT '删除标记',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`ip`,`port`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
