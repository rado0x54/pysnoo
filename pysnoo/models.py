# coding: utf-8
"""PySnoo Data Models."""
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Object holding the user information from Snoo."""

    email: str
    given_name: str
    region: str
    surname: str
    user_id: str

    @staticmethod
    def from_dict(data: dict):
        """Return user object from API response."""
        return User(
            email=data.get("email", ""),
            given_name=data.get("givenName", ""),
            region=data.get("region", ""),
            surname=data.get("surname", ""),
            user_id=data.get("userId", ""),
        )
