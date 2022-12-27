import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_HEADER_TYPE = ""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
