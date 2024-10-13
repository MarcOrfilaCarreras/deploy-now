from flask import Blueprint
from flask import request
from utils.routes import to_json

blueprint = Blueprint('default-500', __name__)


def register_plugin(app):
    app.register_blueprint(blueprint)

    @app.errorhandler(500)
    def handler(e):
        data = {
            "message": "Server error",
            "status": "error"
        }

        return to_json(data)
