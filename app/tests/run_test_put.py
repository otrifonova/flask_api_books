import unittest as ut
from test_put import TestPutMethod
from app import create_app
from config import TestConfig


def no_delete_suite():
    suite = ut.TestSuite()

    suite.addTest(TestPutMethod('test_book'))
    suite.addTest(TestPutMethod('test_author'))
    suite.addTest(TestPutMethod('test_language'))
    suite.addTest(TestPutMethod('test_publisher'))
    suite.addTest(TestPutMethod('test_role'))
    suite.addTest(TestPutMethod('test_edition'))
    suite.addTest(TestPutMethod('test_edition_author'))

    return suite


if __name__ == '__main__':
    runner = ut.TextTestRunner()
    app = create_app(config_class=TestConfig)
    with app.app_context():
        runner.run(no_delete_suite())
