from flask import Blueprint
from flask import render_template

blueprint = Blueprint('_', __name__, template_folder="templates",
                      static_folder="static", static_url_path="/static/_")


def get_homepage():
    return render_template('index.html')


blueprint.add_url_rule('/', view_func=get_homepage, methods=['GET'])


def register_plugin(app):
    app.register_blueprint(blueprint)
