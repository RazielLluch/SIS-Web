import secrets
import cloudinary
from config import LOCAL_SECRET_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from .landing import landing_bp
from .students import students_bp
from .colleges import colleges_bp
from .courses import courses_bp


def register_cloudinary():
    print("CLOUDINARY_CLOUD_NAME:", CLOUDINARY_CLOUD_NAME)
    print("CLOUDINARY_API_KEY:", CLOUDINARY_API_KEY)
    print("CLOUDINARY_API_SECRET:", CLOUDINARY_API_SECRET)

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )


def register_routes(app):
    app.register_blueprint(landing_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(colleges_bp)
    app.register_blueprint(courses_bp)
    app.secret_key = LOCAL_SECRET_KEY
