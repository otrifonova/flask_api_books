import unittest as ut
import requests as req
from test_data import TestData
from token_getter import get_access_token


class TestPutMethod(ut.TestCase):
    _test_data = TestData()
    _status_code = 204

    @classmethod
    def setUpClass(cls) -> None:
        cls._access_token = get_access_token(cls._test_data.test_user_login)

    def put_request(self, url, data):
        return req.put(url, json=data, headers={"Authorization": self._access_token})

    def get_request(self, url):
        return req.get(url, headers={"Authorization": self._access_token})

    def test_book(self):
        url = "http://127.0.0.1:5000/api/book/1"
        r = self.put_request(url, self._test_data.book_1_updated)
        data = self.get_request(url).json()
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(data["title"], self._test_data.book_1_updated["title"])

    def test_author(self):
        url = "http://127.0.0.1:5000/api/author/1"
        r = self.put_request(url, self._test_data.author_1_updated)
        data = self.get_request(url).json()
        del data["id"]
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.author_1_updated, data)

    def test_language(self):
        url = "http://127.0.0.1:5000/api/language/1"
        r = self.put_request(url, self._test_data.language_1_updated)
        data = self.get_request(url).json()
        del data["id"]
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.language_1_updated, data)

    def test_publisher(self):
        url = "http://127.0.0.1:5000/api/publisher/1"
        r = self.put_request(url, self._test_data.publisher_1_updated)
        data = self.get_request(url).json()
        del data["id"]
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.publisher_1_updated, data)

    def test_role(self):
        url = "http://127.0.0.1:5000/api/role/1"
        r = self.put_request(url, self._test_data.role_1_updated)
        data = self.get_request(url).json()
        del data["id"]
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.role_1_updated, data)

    def test_edition(self):
        url = "http://127.0.0.1:5000/api/edition/1"
        r = self.put_request(url, self._test_data.edition_1_updated)
        data = self.get_request(url).json()
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.edition_1_updated["text"], data["text"])

    def test_edition_author(self):
        url = "http://127.0.0.1:5000/api/edition_author/1"
        r = self.put_request(url, self._test_data.edition_author_1_updated)
        data = self.get_request(url).json()
        self.assertEqual(r.status_code, self._status_code)
        self.assertEqual(self._test_data.edition_author_1_updated["order"], data["order"])
