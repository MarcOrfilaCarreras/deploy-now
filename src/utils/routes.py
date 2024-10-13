import datetime
import importlib
import json
import os

from flask import g
from flask import request


def to_json(obj: dict = None):
    if obj is None:
        return {}

    for key in obj.keys():

        if isinstance(obj[key], list):
            obj[key] = list(
                map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, obj[key]))
            continue

        if isinstance(obj[key], object) and hasattr(obj[key], "to_dict"):
            obj[key] = obj[key].to_dict()
            continue

    return json.dumps(obj, indent=2)


def register_blueprints(app, path):
    if app is None:
        return False

    if path is None:
        return False

    for root, dirs, files in os.walk(path):
        for file in files:
            if file == 'entrypoint.py':
                module_name = f"{root.replace(os.sep, '.')}.{file[:-3]}"
                module_blueprint = importlib.import_module(module_name)

                if hasattr(module_blueprint, 'register_plugin'):
                    module_blueprint.register_plugin(app)

    return True


def start_logging(app):

    @app.before_request
    def before_request():
        if not (request.path.startswith('/static/') or request.path.startswith('/favicon')):
            g.start_time = datetime.datetime.now()

            log_data = {
                'timestamp': datetime.datetime.now(),
                'ip': request.headers.getlist('X-Forwarded-For')[0] if request.headers.getlist('X-Forwarded-For') else request.remote_addr,
                'path': request.path,
                'method': request.method,
                'headers': dict(request.headers)
            }

            g.log_data = log_data

    @app.after_request
    def after_request(response):
        if 'log_data' in g:
            execution_time = (datetime.datetime.now() -
                              g.start_time).total_seconds()

            g.log_data['status_code'] = response.status_code
            g.log_data['execution_time'] = execution_time

            with open('requests.log', 'a') as f:
                f.write(
                    f"{g.log_data['timestamp']}, {g.log_data['ip']}, {g.log_data['path']}, {g.log_data['method']}, {g.log_data['status_code']}, {g.log_data['execution_time']} seconds\n")

        return response
