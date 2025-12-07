from flask import Flask
from .config import Config
from .route import hello

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.add_url_rule('/api', 'hello', hello, methods=['GET'])

    return app
