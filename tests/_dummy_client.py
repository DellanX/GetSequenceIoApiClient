"""Shared dummy HTTP response/session helpers for tests."""


class DummyResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json_data = json_data

    async def json(self):
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummySession:
    def __init__(self, response):
        if isinstance(response, list):
            self._responses = list(response)
        else:
            self._responses = [response]
        self.last_request = None

    def request(self, method, url, headers=None, params=None, json=None):
        self.last_request = {"method": method, "url": url, "headers": headers, "params": params, "json": json}
        if not self._responses:
            return DummyResponse(200, {})
        return self._responses.pop(0)
