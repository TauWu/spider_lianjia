# -*- coding: utf-8 -*-
# 本处存放SQL语句模板

import time

local_date = str(time.strftime("%Y-%m-%d", time.localtime()))

print(local_date)

# 房源信息插入SQL语句 - 插入搜索出的房源列表
house_info_insert_sql = """
insert into
    lianjia_house_info(`house_id`, `insert_date`, `house_title`,`community_id`,`community_name`,`house_type`,`house_area`,`orientation`,`distinct_name`,`house_floor`,`house_total_floor`,`house_create_year`,`see_count`,`house_price`,`sale_date`,`extra_info_select`)
values
    ("%s", "{insert_date}", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, %s, "%s", "%s")
""".format(insert_date=str(local_date))

