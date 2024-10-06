import csv
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def read_containers_lock():
    rows = []
    try:
        with open("containers.lock", "r", newline='') as lockfile:
            reader = csv.reader(lockfile)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        return []

    return rows


def write_container_lock(id: str):
    rows = [row for row in read_containers_lock() if row[0] != id]

    rows.append([id, datetime.datetime.now()])

    with open("containers.lock", "w", newline='') as lockfile:
        writer = csv.writer(lockfile)
        writer.writerows(rows)


def delete_container_lock(id: str):
    rows = [row for row in read_containers_lock() if row[0] != id]
    with open("containers.lock", "w", newline='') as lockfile:
        writer = csv.writer(lockfile)
        writer.writerows(rows)


def stop_docker_containers_automatically_job():
    from models.docker.client import Client
    docker_client = Client()

    containers = read_containers_lock()
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"

    for container in containers:
        id, started_str = container[0], container[1]
        started = datetime.datetime.strptime(started_str, datetime_format)

        time_difference = abs(datetime.datetime.now() - started)

        if time_difference >= datetime.timedelta(minutes=1):
            docker_client.stop_container(id=id)
            delete_container_lock(id)


def stop_docker_containers_automatically(interval: int = 10):
    scheduler = BackgroundScheduler()
    scheduler.add_job(stop_docker_containers_automatically_job,
                      "interval", minutes=interval)
    scheduler.start()
