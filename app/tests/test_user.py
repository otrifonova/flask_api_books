import unittest as ut
import requests as req
from test_data import TestData


class TestUser(ut.TestCase):
    _test_data = TestData()

    def test_register(self):
        url = "http://127.0.0.1:5000/api/register"
        r = req.post(url, json=self._test_data.test_user_register)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json().get("message"), f"<User {self._test_data.username}> was created")

    def test_login(self):
        url = "http://127.0.0.1:5000/api/login"
        r = req.post(url, json=self._test_data.test_user_login)
        self.assertEqual(r.json().get("message"), f"Logged in as {self._test_data.username}")
        self.assertEqual(r.status_code, 200)
        if r.status_code == 200:
            data = r.json()
            self.assertEqual(data.get("message"), f"Logged in as {self._test_data.username}")
            self.assertTrue("access_token" in data)
            self.assertTrue("refresh_token" in data)
