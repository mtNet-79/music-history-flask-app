from flask import Flask, current_app

def create_app(test_config=None):
    print("APP create_app()")
    # create and configure the app
    app = Flask(__name__)
    if test_config:
        print("HERE")
        app.config.from_object('config.TestingConfig')
        from models import setup_test_db
        setup_test_db(app)
        # db.app = app
        # db.init_app(app)
    else:
        app.config.from_object('config.Config')
        from models import setup_db
        setup_db(app)
        # db.init_app(app)
        # migrate.init_app(app, db)


    with app.app_context():
        from api import routes
        app.register_blueprint(routes.api)
        return app


