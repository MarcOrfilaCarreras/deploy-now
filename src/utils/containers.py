import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from models.redis.client import Client as RedisClient
from models.redis.db import DB as RedisDB

redis_client = None


def read_containers_lock():
    global redis_client

    if redis_client is None:
        redis_client = RedisClient(
            host=current_app.config["REDIS_HOST"], port=current_app.config["REDIS_HOST_PORT"])
        redis_client.connect(RedisDB.CONTAINERS_LOCK)

    try:
        return redis_client.get(all=True)
    except Exception as e:
        return []


def write_container_lock(id: str) -> bool:
    global redis_client

    if redis_client is None:
        redis_client = RedisClient(
            host=current_app.config["REDIS_HOST"], port=current_app.config["REDIS_HOST_PORT"])
        redis_client.connect(RedisDB.CONTAINERS_LOCK)

    try:
        redis_client.set(id, datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S.%f"))
    except Exception as e:
        return False


def delete_container_lock(id: str):
    global redis_client

    if redis_client is None:
        redis_client = RedisClient(
            host=current_app.config["REDIS_HOST"], port=current_app.config["REDIS_HOST_PORT"])
        redis_client.connect(RedisDB.CONTAINERS_LOCK)

    try:
        redis_client.delete(id)
    except Exception as e:
        return False


def stop_docker_containers_automatically_job():
    from models.docker.client import Client
    docker_client = Client()

    containers = read_containers_lock()
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"

    for container in containers:
        id, started_str = str(container[0].decode(
            "utf-8")), str(container[1].decode("utf-8"))
        started = datetime.datetime.strptime(str(started_str), datetime_format)

        time_difference = abs(datetime.datetime.now() - started)

        if time_difference >= datetime.timedelta(seconds=10):
            docker_client.stop_container(id=id)
            delete_container_lock(id)


def stop_docker_containers_automatically(interval: int = 10):
    scheduler = BackgroundScheduler()
    scheduler.add_job(stop_docker_containers_automatically_job,
                      "interval", seconds=interval)
    scheduler.start()
