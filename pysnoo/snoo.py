"""The main API class"""

from .const import (SNOO_ME_ENDPOINT)
from .auth_session import SnooAuthSession
from .models import User


class Snoo:
    """A Python Abstraction object to Snoo Smart Sleeper Bassinett."""
    # pylint: disable=too-few-public-methods

    def __init__(self, auth: SnooAuthSession):
        """Initialize the Snoo object."""
        self.auth = auth

    async def get_me(self) -> User:
        async with self.auth.get(SNOO_ME_ENDPOINT) as resp:
            assert resp.status == 200
            return await resp.json()
