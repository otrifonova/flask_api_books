import unittest as ut
import requests as req
from test_data import TestData
from token_getter import get_access_token


class TestGetMethod(ut.TestCase):
    _test_data = TestData()
    _status_code = 200

    @classmethod
    def setUpClass(cls) -> None:
        cls._access_token = get_access_token(cls._test_data.test_user_login)

    def get_request(self, url):
        return req.get(url, headers={"Authorization": self._access_token})

    def test_book(self):
        url = "http://127.0.0.1:5000/api/book/1"
        r = self.get_request(url)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json()["id"], 1)

    def test_author(self):
        url = "http://127.0.0.1:5000/api/author/1"
        r = self.get_request(url)
        data = self._test_data.author_1
        data["id"] = 1
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json(), data)

    def test_language(self):
        url = "http://127.0.0.1:5000/api/language/1"
        r = self.get_request(url)
        data = self._test_data.language_1
        data["id"] = 1
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json(), data)

    def test_publisher(self):
        url = "http://127.0.0.1:5000/api/publisher/1"
        r = self.get_request(url)
        data = self._test_data.publisher_1
        data["id"] = 1
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json(), data)

    def test_role(self):
        url = "http://127.0.0.1:5000/api/role/1"
        r = self.get_request(url)
        data = self._test_data.role_1
        data["id"] = 1
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json(), data)

    def test_edition(self):
        url = "http://127.0.0.1:5000/api/edition/1"
        r = self.get_request(url)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json()["id"], 1)

    def test_edition_author(self):
        url = "http://127.0.0.1:5000/api/edition_author/1"
        r = self.get_request(url)
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(r.json()["id"], 1)
