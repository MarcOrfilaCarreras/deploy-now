import docker
import redis
from models.redis.db import DB


class Client(object):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self, db: DB) -> bool:
        self.connection = redis.Redis(
            host=self.host, port=self.port, db=db.value)

    def get(self, id: str = None, all: bool = False):
        if self.connection is None:
            return None

        if all:
            rows = []
            keys = self.connection.keys()

            for key in keys:
                rows.append([key, self.connection.get(key)])

            return rows

        return self.connection.get(id)

    def set(self, id: str, value: str) -> bool:
        if self.connection is None:
            return False

        self.connection.set(id, value)

        return True

    def delete(self, id: str) -> bool:
        if self.connection is None:
            return False

        self.connection.delete(id)

        return True
