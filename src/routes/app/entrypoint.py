import pickle

import requests
from flask import abort
from flask import Blueprint
from flask import request
from flask import Response
from models.docker.client import Client as DockerClient
from models.redis.client import Client as RedisClient
from models.redis.db import DB as RedisDB
from utils.proxy import detect_file_type
from utils.proxy import ProxySession
from utils.proxy import replace_content

blueprint = Blueprint('app-proxy', __name__)

docker_client = DockerClient()
redis_client = None


@blueprint.route('/app/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@blueprint.route('/app/<service>/', defaults={'subpath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(service, subpath):
    container = docker_client.get_container(id=service)

    if not container:
        abort(404)

    target_url = f"http://{container.host}:{container.port}/{subpath}"

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']

    request_headers = {key: value for key, value in request.headers}
    request_params = request.args
    request_data = request.get_data()

    try:
        if redis_client.get(ProxySession.generate_key(request.remote_addr, service)) is None:
            session = ProxySession(request.remote_addr, service)

            if redis_client.set(session.key, session.save_session()) == False:
                raise Exception()

        session = pickle.loads(redis_client.get(
            ProxySession.generate_key(request.remote_addr, service)))
    except Exception as e:
        abort(500)

    try:
        if request.method == 'GET':
            response = session.get(
                target_url, headers=request_headers, params=request_params)
        elif request.method == 'POST':
            response = session.post(
                target_url, headers=request_headers, data=request_data)
        elif request.method == 'PUT':
            response = session.put(
                target_url, headers=request_headers, data=request_data)
        elif request.method == 'DELETE':
            response = session.delete(
                target_url, headers=request_headers, data=request_data)
        elif request.method == 'PATCH':
            response = session.patch(
                target_url, headers=request_headers, data=request_data)
        else:
            return Response('Unsupported HTTP method', status=405)

    except requests.exceptions.ConnectionError:
        abort(404)
    except requests.exceptions.InvalidURL:
        abort(404)

    response_headers = [(name, value) for name, value in response.raw.headers.items(
    ) if name.lower() not in excluded_headers]

    for cookie in session.cookies:
        response_headers.append(
            ('Set-Cookie', f'{cookie.name}={cookie.value}; Path=/'))

    content_type = detect_file_type(target_url)

    if content_type != 'text/html':
        return Response(response.content, response.status_code, response_headers, content_type=content_type)

    return Response(replace_content(response.content, f"/app/{service}"), response.status_code, response_headers, content_type=content_type)


def register_plugin(app):
    app.register_blueprint(blueprint)

    global redis_client
    redis_client = RedisClient(
        host=app.config["REDIS_HOST"], port=app.config["REDIS_HOST_PORT"])
    redis_client.connect(RedisDB.PROXY_SESSIONS)
