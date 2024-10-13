from flask import Blueprint
from flask import request
from utils.routes import to_json

blueprint = Blueprint('default-418', __name__)


def register_plugin(app):
    app.register_blueprint(blueprint)

    @app.errorhandler(415)
    def handler(e):
        data = {
            "message": "I'm a teapot",
            "status": "error"
        }

        return to_json(data)
