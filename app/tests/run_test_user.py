import unittest as ut
from test_user import TestUser
from app import create_app, db
from config import TestConfig


def user_only_suite():
    suite = ut.TestSuite()
    suite.addTest(TestUser('test_register'))
    suite.addTest(TestUser('test_login'))
    return suite


if __name__ == '__main__':
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        runner = ut.TextTestRunner()
        runner.run(user_only_suite())
