from app import create_app
from dotenv import load_dotenv
import os


load_dotenv('.env')

app = create_app()