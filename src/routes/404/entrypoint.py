from flask import Blueprint
from flask import request
from utils.routes import to_json

blueprint = Blueprint('default-404', __name__)


def register_plugin(app):
    app.register_blueprint(blueprint)

    @app.errorhandler(404)
    def handler(e):
        data = {
            "message": "Not found",
            "status": "error"
        }

        return to_json(data)
