import requests as req


def get_access_token(user_data):
    url = "http://127.0.0.1:5000/api/login"
    r = req.post(url, json=user_data)
    data = r.json()
    return data.get("access_token")
