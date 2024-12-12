import secrets
from config import LOCAL_SECRET_KEY
from .landing import landing_bp
from .students import students_bp
from .colleges import colleges_bp
from .courses import courses_bp


def register_routes(app):
    app.register_blueprint(landing_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(colleges_bp)
    app.register_blueprint(courses_bp)
    app.secret_key = LOCAL_SECRET_KEY
