class Production:
    DEBUG = False
    SECRET_KEY = "3d6f45a5fc12445dbac2f59c3b6c7cb1"

    REDIS_HOST = "127.0.0.1"
    REDIS_HOST_PORT = "6379"


class Development:
    DEBUG = True
    SECRET_KEY = "3d6f45a5fc12445dbac2f59c3b6c7cb1"

    REDIS_HOST = "127.0.0.1"
    REDIS_HOST_PORT = "6379"
