# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")

from module.database import DBController

class LJDBController(DBController):

    def __init__(self):
        # 初始化DBController对象
        DBController.__init__(self)

    @property
    def _count(self):
        '''库存数量'''
        from .sql_template import get_count_sql

        DBController.execute(self, get_count_sql)
        count = self.cur.fetchone()[0]
        return count


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
    
    def get_house_ids(self, num=10):
        '''向数据库请求num数量的房间ID'''
        from .sql_template import get_house_id_sql
        
        count = self._count

        for t in range(0, int(count/num) + 1):
            id_list = list()
            if t != int(count/num):
                for i in range(1, num + 1):
                    id_list.append(str(t * num + i))
            else:
                for i in range(int(count/num)*num, count+1):
                    id_list.append(str(i))
            id_list = ",".join(id_list)
            DBController.execute(self, get_house_id_sql%(id_list))

            house_id_list = self.cur.fetchall()

            yield (house_id_list)

    def update_house_info(self, house_info_list):
        '''将房间详情页面的信息'''
        from .sql_template import update_house_info_sql

        for house_info in house_info_list:
            try:
                update_house_info_sql_exec = (update_house_info_sql.format(house_id=house_info[0]))%(tuple(house_info[1:]))
                DBController.execute(self, update_house_info_sql_exec)
                print("更新房源【%s】详情成功"%house_info[0])
            except Exception as e:
                print("更新页面详情数据错误", e, update_house_info_sql_exec)

    @property
    def close(self):
        '''关闭数据库连接'''
        DBController.close