from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # type: ignore
from typing import Optional

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config: Optional[str] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, template_folder='templates')
    if test_config:
        app.config.from_object('config.TestingConfig')
        db.init_app(app)
    else:
        app.config.from_object('config.DevelopmentConfig')
        db.init_app(app)
        migrate.init_app(app, db, compare_type=True)

    with app.app_context():
        if test_config:
            db.create_all()
        from .routes import api
        app.register_blueprint(api)

        return app
# from .models.performer import Performer
# from .models.recording import Recording
# from .models.tables import (contemporaries, composer_performer,
# composer_style, performer_style, composer_title, performer_title)
# from .models.style import Style
# from .models.period import Period
# from .models.composition import Composition
# from .models.composer import Composer
