import cloudinary
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from flask import Flask
from .controller import register_routes, register_cloudinary


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    register_cloudinary()

    register_routes(app)

    return app
