import os
import redis


class HerokuRedisQueue:
    def __init__(self, name, namespace="printer"):
        self.__db = redis.from_url(os.environ.get("REDIS_URL"))
        self.key = f"{namespace}:{name}"

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get(self):
        item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item
