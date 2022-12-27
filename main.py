from app import create_app
from config import TestConfig

app = create_app(TestConfig)
