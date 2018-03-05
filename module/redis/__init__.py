# -*- coding: utf-8 -*-

from ..database import LJDBController

import sys
sys.path.append("../..")

from util.redis import RedisController

class LJRedisController():

    def __init__(self):
        self._db = LJDBController()
        self._redis = RedisController()

    def failed_page_insert(self):
        '''将spider_page操作中执行失败的房源编号列表入Redis'''
        house_list = self._db.get_house_page_failed
        for id in range(0,len(house_list)):
            idx = id + 1
            self._redis.rset(str(idx),house_list[id])
    
    def failed_page_get(self, num=20):
        '''将Redis中存储的房源ID按照num的频次返回'''
        for id in range(0, self._redis.dbsize, 20):
            house_list_get = list()
            for i in range(0 ,20):
                idx = id + i + 1
                house_id = self._redis.rget(str(idx))
                if house_id.strip() == "n":
                    pass
                else:
                    house_list_get.append((idx, house_id))
            yield house_list_get

    def success_page_del(self, house_list):
        '''将更小粒度执行完成的一组房源编号从Redis中删除'''
        for house_id in house_list:
            self.page_reexec_del(house_id[0])

    def page_reexec_del(self, key):
        '''将重新运行过的房源编号从Redis中删除'''
        self._redis.rdel(key)

    @property
    def close(self):
        '''一些需要最终处理的事务'''
        self._db.close