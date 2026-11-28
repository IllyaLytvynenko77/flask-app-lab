from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from app.config import config


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    db.init_app(app)
    migrate.init_app(app, db)

    from app.products import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    from app.products import models  # noqa: F401

    @app.route("/")
    def index():
        return "Lab 7: SQLAlchemy Relationships & Migrations"

    return app
