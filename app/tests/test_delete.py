import unittest as ut
import requests as req
from test_data import TestData
from token_getter import get_access_token


class TestDeleteMethod(ut.TestCase):
    _test_data = TestData()
    _status_code = 204

    @classmethod
    def setUpClass(cls) -> None:
        cls._access_token = get_access_token(cls._test_data.test_user_login)

    def delete_request(self, url):
        return req.delete(url, headers={"Authorization": self._access_token})

    def get_request(self, url):
        return req.get(url, headers={"Authorization": self._access_token})

    def test_edition_author(self):
        url = "http://127.0.0.1:5000/api/edition_author/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

        url = "http://127.0.0.1:5000/api/edition_author/2"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_edition(self):
        url = "http://127.0.0.1:5000/api/edition/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_author(self):
        url = "http://127.0.0.1:5000/api/author/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_language(self):
        url = "http://127.0.0.1:5000/api/language/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_publisher(self):
        url = "http://127.0.0.1:5000/api/publisher/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_role(self):
        url = "http://127.0.0.1:5000/api/role/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)

    def test_book(self):
        url = "http://127.0.0.1:5000/api/book/1"
        r = self.delete_request(url)
        self.assertEqual(r.status_code, self._status_code)
        r = self.get_request(url)
        self.assertEqual(r.status_code, 404)
        r = self.get_request("http://127.0.0.1:5000/api/edition/2")
        self.assertEqual(r.status_code, 404)
        r = self.get_request("http://127.0.0.1:5000/api/edition_author/3")
        self.assertEqual(r.status_code, 404)
