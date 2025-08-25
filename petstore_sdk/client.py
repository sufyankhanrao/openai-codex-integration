"""High level Petstore client."""
from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from .config import ClientConfig
from .http import HTTPTransport, RequestsTransport
from .models import Pet


class PetstoreClient:
    """Client for interacting with the Petstore API."""

    def __init__(self, config: ClientConfig, transport: Optional[HTTPTransport] = None):
        self.config = config
        self.transport = transport or RequestsTransport(config)

    def list_pets(self, limit: Optional[int] = None) -> List[Pet]:
        params = {"limit": limit} if limit is not None else None
        url = f"{self.config.base_url}/pets"
        response = self.transport.request("GET", url, params=params)
        return [Pet(**p) for p in response.json()]

    def create_pet(self, pet: Pet) -> None:
        url = f"{self.config.base_url}/pets"
        self.transport.request("POST", url, json=asdict(pet))

    def get_pet(self, pet_id: str) -> Pet:
        url = f"{self.config.base_url}/pets/{pet_id}"
        response = self.transport.request("GET", url)
        return Pet(**response.json())
