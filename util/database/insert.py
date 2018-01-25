# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

from module.database import db_conn

def insert_lianjia_house_json(lianjia_houseinfo):
    insert_sql = """
    insert into 
        lianjia_house_info_json
        (`house_id`, `house_info`)
    values
        ("%s", "%s")
    """
    try:
        conn, cur = db_conn()
        cur.execute(insert_sql%(lianjia_houseinfo["HouseID"], str(lianjia_houseinfo)))
    finally:
        cur.close()
        conn.close()