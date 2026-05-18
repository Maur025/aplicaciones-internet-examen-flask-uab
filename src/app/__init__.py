from flask import Flask

import config
from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        from . import models

        appbuilder.init_app(app, db.session)
        db.create_all()

        from . import views

    return app
