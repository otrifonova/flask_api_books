import unittest as ut
from test_get import TestGetMethod
from app import create_app
from config import TestConfig


def get_suite():
    suite = ut.TestSuite()

    suite.addTest(TestGetMethod('test_book'))
    suite.addTest(TestGetMethod('test_author'))
    suite.addTest(TestGetMethod('test_language'))
    suite.addTest(TestGetMethod('test_publisher'))
    suite.addTest(TestGetMethod('test_role'))
    suite.addTest(TestGetMethod('test_edition'))
    suite.addTest(TestGetMethod('test_edition_author'))

    return suite


if __name__ == '__main__':
    runner = ut.TextTestRunner()
    app = create_app(config_class=TestConfig)
    with app.app_context():
        runner.run(no_delete_suite())
