from flask import Flask
from .config import Config
from .extensions import db, migrate
from .main import main
from .api import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # db.init_app(app)
    # migrate.init_app(db, app)

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app