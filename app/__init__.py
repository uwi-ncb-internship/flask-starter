from flask import Flask
import click
from .config import Config
from .extensions import db, migrate
from .main import main
from .api import api
from seed import seed_data

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command()
    def seed():
        seed_data()
        click.echo("Database Seeded.")

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app