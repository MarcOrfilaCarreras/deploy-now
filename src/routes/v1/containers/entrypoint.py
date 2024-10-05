from flask import abort
from flask import Blueprint
from flask import request
from models.docker.client import Client
from models.docker.container import ContainerState
from utils.routes import to_json

blueprint = Blueprint('v1-containers', __name__)

docker_client = Client()


def get_containers():
    if request.method != 'GET':
        abort(405)

    data = {
        "containers": docker_client.get_containers(),
        "status": "success"
    }

    return to_json(data)


def container_router(id: str):
    if request.method == 'GET':
        return get_container(id)

    if request.method == 'PATCH':
        return patch_container(id)

    abort(405)


def get_container(id: str):
    container = docker_client.get_container(id=id)

    if not container:
        abort(404)

    data = {
        "container": container,
        "status": "success"
    }

    return to_json(data)


def patch_container(id: str):
    container = docker_client.get_container(id=id)

    if not container:
        abort(404)

    # TODO: Parse the options correctly
    options = request.get_json()

    if (options["state"]) and (not container.patch_state(state=ContainerState.from_string(options["state"]))):
        data = {
            "message": "The container could not be patched",
            "status": "error"
        }

        return to_json(data)

    data = {
        "container": container,
        "status": "success"
    }

    return to_json(data)


blueprint.add_url_rule('/api/v1/containers',
                       view_func=get_containers, methods=['GET'])
blueprint.add_url_rule('/api/v1/containers/<string:id>',
                       view_func=container_router, methods=['GET'])
blueprint.add_url_rule('/api/v1/containers/<string:id>',
                       view_func=container_router, methods=['PATCH'])


def register_plugin(app):
    app.register_blueprint(blueprint)
