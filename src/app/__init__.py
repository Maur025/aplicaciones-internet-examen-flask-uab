import os

from flask import Flask

import config
from .extensions import appbuilder, db
from .socket_client import connect_socket_client


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        from . import models

        appbuilder.init_app(app, db.session)
        db.create_all()

        from . import views

        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            connect_socket_client(app)

    return app
