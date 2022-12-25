import unittest as ut
import requests as req
from test_data import TestData
from token_getter import get_access_token


class TestPostMethod(ut.TestCase):
    _test_data = TestData()
    _status_code = 201

    @classmethod
    def setUpClass(cls) -> None:
        cls._access_token = get_access_token(cls._test_data.test_user_login)

    def post_request(self, url, data):
        return req.post(url, json=data, headers={"Authorization": self._access_token})

    def test_book(self):
        url = "http://127.0.0.1:5000/api/book"
        r = self.post_request(url, self._test_data.book_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

    def test_author(self):
        url = "http://127.0.0.1:5000/api/author"
        r = self.post_request(url, self._test_data.author_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.author_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

    def test_language(self):
        url = "http://127.0.0.1:5000/api/language"
        r = self.post_request(url, self._test_data.language_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.language_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

    def test_publisher(self):
        url = "http://127.0.0.1:5000/api/publisher"
        r = self.post_request(url, self._test_data.publisher_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.publisher_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

    def test_role(self):
        url = "http://127.0.0.1:5000/api/role"
        r = self.post_request(url, self._test_data.role_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.role_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

    def test_edition(self):
        url = "http://127.0.0.1:5000/api/edition"
        r = self.post_request(url, self._test_data.edition_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.edition_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

    def test_edition_author(self):
        url = "http://127.0.0.1:5000/api/edition_author"
        r = self.post_request(url, self._test_data.edition_author_1)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/1")

        r = self.post_request(url, self._test_data.edition_author_2)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/2")

        r = self.post_request(url, self._test_data.edition_author_3)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.headers['Location'], url[21:] + "/3")
