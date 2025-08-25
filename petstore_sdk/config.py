"""Configuration objects for the Petstore SDK."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union

# Hooks allow users to tap into the request/response life cycle.
RequestHook = Callable[[str, str, Dict[str, Any]], None]
ResponseHook = Callable[[Any], None]


@dataclass
class ClientConfig:
    """Settings for :class:`petstore_sdk.client.PetstoreClient`.

    Attributes:
        base_url: Target server for API calls.
        timeout: Default timeout (seconds) for HTTP requests.
        retries: Number of automatic retries for failed requests.
        pre_request: Optional hook invoked before a request is sent.
        post_response: Optional hook invoked after a response is received.
    """

    base_url: str = "https://petstore.swagger.io/v1"
    timeout: Union[float, Tuple[float, float]] = 5.0
    retries: int = 3
    pre_request: Optional[RequestHook] = None
    post_response: Optional[ResponseHook] = None
