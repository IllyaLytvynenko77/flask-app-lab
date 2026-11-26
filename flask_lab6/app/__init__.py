from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from app.config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Імпорт моделей для коректної роботи Flask-Migrate
    from app import models  # noqa: F401
    from app.posts import models as post_models  # noqa: F401

    # Реєстрація блюпринта постів
    from app.posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/post")

    @app.route("/", endpoint="home")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
