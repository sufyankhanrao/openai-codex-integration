"""Data models for the Petstore API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    """Represents a pet object."""

    id: int
    name: str
    tag: Optional[str] = None


@dataclass
class Error:
    """Represents an API error."""

    code: int
    message: str
