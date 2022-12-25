from app import create_app, db
from config import TestConfig


app = create_app(config_class=TestConfig)
with app.app_context():
    db.drop_all()
