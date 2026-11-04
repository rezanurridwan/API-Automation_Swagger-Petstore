import requests

from Config.config import BASE_URL, HEADERS, TIMEOUT


class APIClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def post(self, endpoint, payload):
        return self.session.post(
            f"{BASE_URL}{endpoint}",
            json=payload,
            timeout=TIMEOUT
        )

    def get(self, endpoint):
        return self.session.get(
            f"{BASE_URL}{endpoint}",
            timeout=TIMEOUT
        )

    def put(self, endpoint, payload):
        return self.session.put(
            f"{BASE_URL}{endpoint}",
            json=payload,
            timeout=TIMEOUT
        )

    def close(self):
        self.session.close()
