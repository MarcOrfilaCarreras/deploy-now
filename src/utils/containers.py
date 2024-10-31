import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from models.redis.client import Client as RedisClient
from models.redis.db import DB as RedisDB

redis_client = None


class ContainersLock(object):
    client = None

    def __init__(self):
        if ContainersLock.client is None:
            ContainersLock.client = RedisClient(
                host=current_app.config["REDIS_HOST"], port=current_app.config["REDIS_HOST_PORT"])
            ContainersLock.client.connect(RedisDB.CONTAINERS_LOCK)

    def read(self):
        try:
            return ContainersLock.client.get(all=True)
        except Exception as e:
            return []

    def write(self, id: str):
        try:
            ContainersLock.client.set(
                id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        except Exception as e:
            return False

    def delete(self, id: str):
        try:
            ContainersLock.client.delete(id)
        except Exception as e:
            return False


def stop_docker_containers_automatically_job():
    from models.docker.client import Client
    docker_client = Client()
    containers_lock = ContainersLock()

    containers = containers_lock.read()
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"

    for container in containers:
        id, started_str = str(container[0].decode(
            "utf-8")), str(container[1].decode("utf-8"))
        started = datetime.datetime.strptime(str(started_str), datetime_format)

        time_difference = abs(datetime.datetime.now() - started)

        if time_difference >= datetime.timedelta(minutes=10):
            docker_client.stop_container(id=id)
            containers_lock.delete(id)


def stop_docker_containers_automatically(interval: int = 10):
    scheduler = BackgroundScheduler()
    scheduler.add_job(stop_docker_containers_automatically_job,
                      "interval", minutes=interval)
    scheduler.start()
