# -*- coding: utf-8 -*-
# 本处存放SQL语句模板

import time

local_date = str(time.strftime("%Y-%m-%d", time.localtime()))

print(local_date)

# 房源信息插入SQL语句 - 插入搜索出的房源列表
house_info_insert_sql = """
insert into
    lianjia_house_info(`house_id`, `insert_date`, `house_title`,
    `community_id`,`community_name`,`house_type`,`house_area`,
    `orientation`,`distinct_name`,`house_floor`,`house_total_floor`,
    `house_create_year`,`see_count`,`house_price`,`sale_date`,
    `extra_info_select`)
values
    ("%s", "{insert_date}", "%s", "%s", 
    "%s", "%s", "%s", "%s", "%s", "%s",
    "%s", "%s", %s, %s, "%s", "%s")
""".format(insert_date=str(local_date))

# 获取库存总量SQL
get_count_sql = """
select
    count(1)
from
    lianjia_house_info
"""

# 批量请求房源ID的SQL
get_house_id_sql = """
select
    house_id
from
    lianjia_house_info
where
    id in ( %s )
"""

# 批量请求房源ID+地标ID的SQL
get_hc_id_sql = """
select
    house_id, community_id
from
    lianjia_house_info
where
    id in ( %s )
"""

# 更新房源详情数据SQL
update_house_info_sql = """
update
    lianjia_house_info
set
    house_type_new = "%s" , sale_date_new = "%s" ,
    basic_info = "%s" , house_tags = "%s" , 
    house_feature = "%s"
where
    house_id = "{house_id}"
"""