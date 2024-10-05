import requests
from flask import abort
from flask import Blueprint
from flask import request
from flask import Response
from models.docker.client import Client

blueprint = Blueprint('proxy', __name__)

docker_client = Client()


@blueprint.route('/app/<id>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@blueprint.route('/app/<id>/', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(id, subpath):
    container = docker_client.get_container(id=id)

    if not container:
        abort(404)

    target_url = f"http://{container.host}:{container.port}/{subpath}"

    headers = {key: value for key, value in request.headers}
    data = request.get_data()

    try:
        if request.method == 'GET':
            response = requests.get(
                target_url, headers=headers, params=request.args)
        elif request.method == 'POST':
            response = requests.post(target_url, headers=headers, data=data)
        elif request.method == 'PUT':
            response = requests.put(target_url, headers=headers, data=data)
        elif request.method == 'DELETE':
            response = requests.delete(target_url, headers=headers, data=data)
        elif request.method == 'PATCH':
            response = requests.patch(target_url, headers=headers, data=data)
        else:
            return Response('Unsupported HTTP method', status=405)
    except requests.exceptions.ConnectionError:
        abort(404)
    except requests.exceptions.InvalidURL:
        abort(404)

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items(
    ) if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)


def register_plugin(app):
    app.register_blueprint(blueprint)
