import docker
from models.docker.container import Container
from models.docker.container import ContainerState
from utils.containers import delete_container_lock
from utils.containers import write_container_lock


class Client(object):
    def __init__(self):
        self.env = docker.from_env()

    def get_container(self, *, id: str = None):
        if id is None:
            return None

        try:
            container = self.env.containers.get(id)

            if not ("deploy-now.enable" in container.labels.keys()):
                return None

            if not (container.labels.get("deploy-now.enable").lower() == "true"):
                return None

            network_settings = None if container.ports == {
            } else container.ports[list(container.ports.keys())[0]][0]

            return Container(
                id=container.id,
                name=container.name,
                state=ContainerState.from_string(container.status),
                host="" if network_settings is None else network_settings["HostIp"],
                port=0 if network_settings is None else int(
                    network_settings["HostPort"]),
                description="" if not "deploy-now.description" in container.labels.keys(
                ) else container.labels.get("deploy-now.description")
            )

        except docker.errors.DockerException as e:
            return None

    def start_container(self, *, id: str = None) -> bool:
        if id is None:
            return None

        try:
            container = self.env.containers.get(id)

            container.start()

            write_container_lock(container.id)

            return True

        except docker.errors.DockerException as e:
            return False

    def stop_container(self, *, id: str = None) -> bool:
        if id is None:
            return None

        try:
            container = self.env.containers.get(id)

            container.stop()

            delete_container_lock(id)

            return True

        except docker.errors.DockerException as e:
            return False

    def stop_containers(self):
        try:
            for container in self.env.containers.list(all=True):
                if self.get_container(id=container.id) is not None:
                    self.stop_container(id=container.id)
        except docker.errors.DockerException as e:
            exit(1)

    def get_containers(self):
        try:
            containers = []

            for container in self.env.containers.list(all=True):
                if self.get_container(id=container.id) is not None:
                    containers.append(self.get_container(id=container.id))

            return containers
        except docker.errors.DockerException as e:
            return None
