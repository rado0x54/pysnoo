# coding: utf-8
"""PySnoo Data Models."""
from dataclasses import dataclass


@dataclass
class User:
    """Object holding the user information from Snoo."""

    email: str
    givenName: str
    region: str
    surname: str
    userId: str

    @staticmethod
    def from_dict(data: dict):
        """Return user object from API response."""
        return User(**data)

