from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from .landing import landing_bp as landing_blueprint
    app.register_blueprint(landing_blueprint)

    return app