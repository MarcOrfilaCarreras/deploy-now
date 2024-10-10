import json
from enum import Enum

import docker


class ContainerState(Enum):
    CREATED = "created"
    RESTARTING = "restarting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    EXITED = "exited"

    @staticmethod
    def from_string(state_str):
        try:
            return ContainerState[state_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown container status: {state_str}")

    def __str__(self):
        return self.value


class Container(object):
    def __init__(self, *, id: str = None, name: str = None, state: ContainerState = None, host: str, port: int, description: str = ""):
        self.id = id
        self.name = name
        self.state = state
        self.host = host
        self.port = port
        self.description = description

    def patch_state(self, *, state: ContainerState = None) -> bool:
        if state is None:
            return False

        from models.docker.client import Client

        if state is ContainerState.RUNNING:
            try:
                docker_client = Client()

                return docker_client.start_container(id=self.id)
            except docker.errors.DockerException as e:
                return False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state.value,
            "description": self.description
        }

    def to_json(self):
        return json.dumps(self.to_dict())
