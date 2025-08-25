import os
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from petstore_sdk import ClientConfig, Pet, PetstoreClient, RequestsTransport


def test_list_pets_hooks(monkeypatch):
    config = ClientConfig(base_url="https://example.com")
    called = {"pre": False, "post": False}

    def pre(method, url, kwargs):
        called["pre"] = True
        assert method == "GET"
        assert url.endswith("/pets")

    def post(response):
        called["post"] = True

    config.pre_request = pre
    config.post_response = post

    transport = RequestsTransport(config)
    dummy_response = SimpleNamespace()
    dummy_response.json = lambda: [{"id": 1, "name": "Dog"}]
    dummy_response.raise_for_status = lambda: None

    monkeypatch.setattr(transport.session, "request", MagicMock(return_value=dummy_response))

    client = PetstoreClient(config, transport=transport)
    pets = client.list_pets(limit=1)

    assert pets == [Pet(id=1, name="Dog")]
    assert called["pre"] and called["post"]
    transport.session.request.assert_called_once()
    _, _, kwargs = transport.session.request.mock_calls[0]
    assert kwargs["timeout"] == config.timeout
