import unittest as ut
from run_test_user import user_only_suite
from run_test_post import post_suite
from run_test_get import get_suite
from run_test_put import put_suite
from run_test_delete import delete_suite
from app import create_app, db
from config import TestConfig


if __name__ == '__main__':
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        runner = ut.TextTestRunner()
        runner.run(user_only_suite())
        runner.run(post_suite())
        runner.run(get_suite())
        runner.run(put_suite())
        runner.run(delete_suite())
        db.drop_all()
