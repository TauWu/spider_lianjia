# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")

from module.database import DBController

class LJDBController(DBController):

    def __init__(self):
        # 初始化DBController对象
        DBController.__init__(self)

    def insert_house(self, house_info_list):
        '''向house_info表中插入多条房源信息'''
        from .sql_template import house_info_insert_sql

        for house_info in house_info_list:
            try:
                DBController.execute(self, house_info_insert_sql%(tuple(house_info)))
                print("插入房间【%s】成功"%house_info[0])
            except self.IntegrityError:
                print("忽略插入重复【%s】"%house_info[0])
            except Exception as e:
                print("未知错误！输出house_info待确定【%s】"%house_info[0], house_info, e)
    
    @property
    def close(self):
        '''关闭数据库连接'''
        DBController.close