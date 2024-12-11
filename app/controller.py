from .landing import landing_bp
from .students import students_bp


def register_routes(app):
    app.register_blueprint(landing_bp)
    app.register_blueprint(students_bp)