
from oauthlib.oauth2 import LegacyApplicationClient

from .oauth.oauth2_session import OAuth2Session
from pysnoo.const import (OAuth)


class SnooAuthSession(OAuth2Session):
    """Snoo-specific OAuth2 Session Object"""

    def __init__(
            self, token=None, token_updater=None):
        """Construct a new OAuth 2 client session."""

        # From Const
        super(SnooAuthSession, self).__init__(
            client=LegacyApplicationClient(client_id=OAuth.CLIENT_ID),
            auto_refresh_url=OAuth.TOKEN_REFRESH_ENDPOINT,
            auto_refresh_kwargs=None,
            scope=None,
            redirect_uri=None,
            token=token,
            state=None,
            token_updater=token_updater)

    async def fetch_token(
            self, username, password):
        return await super().fetch_token(OAuth.LOGIN_ENDPOINT, code=None, authorization_response=None,
            body='', auth=None, username=username, password=password, method='POST',
            timeout=None, headers=None, verify_ssl=True)

