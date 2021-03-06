# coding:utf-8
import time
import json
import redis
import settings
import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('mylogger')


class RedisObj():
    def __init__(self):
        self.__redis_host = settings.redis_con.get('ip')
        self.__redis_port = settings.redis_con.get('port')
        self.__redis_db = settings.redis_con.get('db')
        self.__redis_auth = settings.redis_con.get('auth')
        self.redis_sleep_time = settings.no_task_sleep_time

    def get_redis_pool(self):
        redis_handler = redis.ConnectionPool(host=self.__redis_host,
                                             port=self.__redis_port,
                                             db=self.__redis_db,
                                             password=self.__redis_auth)
        return redis_handler

    def get_task(self, key):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        task_info = redis_con.lpop(key)
        if task_info:
            task_info = json.loads(task_info)
        return task_info

    def push_task(self, key, data, reverse=False):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        data = json.dumps(data)
        if reverse:
            redis_con.lpush(key, data)
        else:
            redis_con.rpush(key, data)

    def delete_task(self, key, data):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        data = json.dumps(data)
        redis_con.lrem(key, data, 1)

    def get_task_count(self, key):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        return redis_con.llen(key)

    def add_set(self, key, data):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        data = json.dumps(data)
        return redis_con.sadd(key, data)

    def rem_set(self, key, data):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        data = json.dumps(data)
        return redis_con.srem(key, data)

    def del_key(self, key):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        redis_con.delete(key)

    def random_member(self, key):
        redis_con = redis.Redis(connection_pool=self.get_redis_pool())
        task_info = redis_con.srandmember(key)
        task_info = json.loads(task_info)
        return task_info
