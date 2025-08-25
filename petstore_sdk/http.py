"""HTTP transport abstractions for the Petstore SDK."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ClientConfig, RequestHook, ResponseHook


class HTTPTransport(ABC):
    """Abstract base class for HTTP communication."""

    def __init__(self, config: ClientConfig):
        self.config = config

    @abstractmethod
    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Perform an HTTP request and return a response."""


class RequestsTransport(HTTPTransport):
    """`HTTPTransport` implementation using :mod:`requests`.

    Handles retries, timeouts and supports request/response hooks.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.session = requests.Session()
        retry_strategy = Retry(
            total=config.retries,
            status_forcelist=(500, 502, 503, 504),
            backoff_factor=0.5,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        hooks: Dict[str, Any] = kwargs.setdefault("hooks", {})
        if self.config.pre_request:
            self.config.pre_request(method, url, kwargs)
        timeout = kwargs.pop("timeout", self.config.timeout)
        response = self.session.request(method, url, timeout=timeout, **kwargs)
        if self.config.post_response:
            self.config.post_response(response)
        response.raise_for_status()
        return response
