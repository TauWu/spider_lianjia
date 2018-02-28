# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")

from module.database import DBController

class LJDBController(DBController):

    def __init__(self):
        # 初始化DBController对象
        DBController.__init__(self)

    def _count(self, start=0):
        '''库存数量'''
        from .sql_template import get_count_sql

        DBController.execute(self, get_count_sql)
        count = self.cur.fetchone()[0]
        return count - start


    def insert_house(self, district, house_info_list):
        '''向house_info表中插入多条房源信息'''
        from .sql_template import house_info_insert_sql, local_date

        for house_info in house_info_list:
            try:
                DBController.execute(self, (house_info_insert_sql.format(district=district, insert_date=str(local_date)))%(tuple(house_info)))
                print("插入房间【%s】成功"%house_info[0])
            except self.IntegrityError:
                print("忽略插入重复【%s】"%house_info[0])
            except Exception as e:
                print("未知错误！输出house_info待确定【%s】"%house_info[0], house_info, e)
    
    def get_house_ids(self, start=0, num=80):
        '''向数据库请求num数量的房间ID'''
        from .sql_template import get_house_id_sql
        
        count = self._count(start=start)

        for t in range(0, int(count/num) + 1):
            id_list = list()
            if t != int(count/num):
                for i in range(1, num + 1):
                    id_list.append(str(start + t * num + i))
            else:
                for i in range(int(count/num)*num, count+1):
                    id_list.append(str(start + i))
            id_list = ",".join(id_list)
            DBController.execute(self, get_house_id_sql%(id_list))

            house_id_list = self.cur.fetchall()

            yield (house_id_list)

    def get_hc_ids(self, start=0, num=80):
        '''向数据库请求num数量的房间ID+地标ID'''
        from .sql_template import get_hc_id_sql
        
        count = self._count(start=start)

        for t in range(0, int(count/num) + 1):
            id_list = list()
            if t != int(count/num):
                for i in range(1, num + 1):
                    id_list.append(str(start + t * num + i))
            else:
                for i in range(int(count/num)*num, count+1):
                    id_list.append(str(start + i))
            id_list = ",".join(id_list)
            DBController.execute(self, get_hc_id_sql%(id_list))

            hc_id_list = self.cur.fetchall()

            yield (hc_id_list)

    def update_house_info(self, house_info_list):
        '''将房间详情页面的信息'''
        from .sql_template import update_house_info_sql

        for house_info in house_info_list:
            update_house_info_sql_exec = str()
            try:
                update_house_info_sql_exec = (update_house_info_sql.format(house_id=house_info[0]))%(tuple(house_info[1:]))
                DBController.execute(self, update_house_info_sql_exec)
                print("更新房源【%s】详情成功"%house_info[0])
            except IndexError:
                print("[IndexError]更新页面详情数据错误", house_info)
            except Exception as e:
                print("更新页面详情数据错误", e, update_house_info_sql_exec)
                

    def update_house_stat(self, house_stat_list):
        '''更新房间统计信息'''
        from .sql_template import update_house_stat_sql, insert_house_stat_json_sql

        for house_stat in house_stat_list:
            try:
                update_house_stat_sql_exec = (update_house_stat_sql.format(house_id=house_stat[0]))%(tuple(house_stat[1:-1]))
                DBController.execute(self, update_house_stat_sql_exec)
                DBController.execute(self, insert_house_stat_json_sql%(tuple([house_stat[0]]+[house_stat[-1]])))
                print("更新房源【%s】统计成功"%house_stat[0])
            except self.IntegrityError:
                print("重复的插入统计表【%s】"%house_stat[0])
            except Exception as e:
                print("更新统计信息错误", e, update_house_stat_sql_exec)

    @property
    def close(self):
        '''关闭数据库连接'''
        DBController.close