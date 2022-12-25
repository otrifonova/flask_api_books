import unittest as ut
from test_delete import TestDeleteMethod
from app import create_app
from config import TestConfig


def delete_suite():
    suite = ut.TestSuite()
    suite.addTest(TestDeleteMethod('test_edition_author'))
    suite.addTest(TestDeleteMethod('test_edition'))
    suite.addTest(TestDeleteMethod('test_author'))
    suite.addTest(TestDeleteMethod('test_language'))
    suite.addTest(TestDeleteMethod('test_publisher'))
    suite.addTest(TestDeleteMethod('test_role'))
    suite.addTest(TestDeleteMethod('test_book'))

    return suite


if __name__ == '__main__':
    runner = ut.TextTestRunner()
    app = create_app(config_class=TestConfig)
    with app.app_context():
        runner.run(delete_suite())
