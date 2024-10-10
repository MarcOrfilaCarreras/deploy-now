import sentry_sdk
from config import Development
from config import Production
from flask import Flask
from models.docker.client import Client
from utils.containers import stop_docker_containers_automatically
from utils.routes import register_blueprints
from utils.routes import start_logging

sentry_sdk.init(
    dsn="https://e36f3f6966e66c8d5a0ab6a1ba0a3458@o4508100162486272.ingest.de.sentry.io/4508100164649040",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

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
