from config import Development
from config import Production
from flask import Flask
from models.docker.client import Client
from utils.containers import stop_docker_containers_automatically
from utils.routes import register_blueprints
from utils.routes import start_logging


app = Flask(__name__)
app.config.from_object(Production)

register_blueprints(app=app, path="routes")

start_logging(app=app)

docker_client = Client()

with app.app_context():
    stop_docker_containers_automatically()
    docker_client.stop_containers()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
