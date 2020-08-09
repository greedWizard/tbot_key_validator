from flask import Flask

from .extensions import db
import server_api.config as config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(getattr(config, os.getenv('TBOT_CONFIG', 'Dev')))

    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    return app