from flask import Blueprint
from flask import request
from utils.routes import to_json

blueprint = Blueprint('default-405', __name__)


def register_plugin(app):
    app.register_blueprint(blueprint)

    @app.errorhandler(405)
    def handler(e):
        data = {
            "message": "Method not allowed",
            "status": "error"
        }

        return to_json(data)
