import unittest as ut
from test_post import TestPostMethod
from app import create_app
from config import TestConfig


def no_delete_suite():
    suite = ut.TestSuite()

    suite.addTest(TestPostMethod('test_book'))
    suite.addTest(TestPostMethod('test_author'))
    suite.addTest(TestPostMethod('test_language'))
    suite.addTest(TestPostMethod('test_publisher'))
    suite.addTest(TestPostMethod('test_role'))
    suite.addTest(TestPostMethod('test_edition'))
    suite.addTest(TestPostMethod('test_edition_author'))

    return suite


if __name__ == '__main__':
    runner = ut.TextTestRunner()
    app = create_app(config_class=TestConfig)
    with app.app_context():
        runner.run(no_delete_suite())
