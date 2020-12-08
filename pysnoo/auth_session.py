# coding: utf-8
"""PySnoo OAuth Session."""

import json
from typing import Type
from oauthlib.oauth2 import LegacyApplicationClient

from .const import (OAUTH_CLIENT_ID,
                    OAUTH_TOKEN_REFRESH_ENDPOINT,
                    OAUTH_LOGIN_ENDPOINT)
from .oauth.oauth2_session import OAuth2Session


class SnooAuthSession(OAuth2Session):
    """Snoo-specific OAuth2 Session Object"""

    def __init__(
            self, token=None, token_updater=None):
        """Construct a new OAuth 2 client session."""

        # From Const
        super().__init__(
            client=LegacyApplicationClient(client_id=OAUTH_CLIENT_ID),
            auto_refresh_url=OAUTH_TOKEN_REFRESH_ENDPOINT,
            auto_refresh_kwargs=None,
            scope=None,
            redirect_uri=None,
            token=token,
            state=None,
            token_updater=token_updater)

    def __init_subclass__(cls: Type["SnooAuthSession"]) -> None:
        """Overwrite to suppress warning in base class"""
        return

    async def fetch_token(self, username, password):  # pylint: disable=arguments-differ
        # Note, Snoo OAuth API is not 100% RFC 6749 compliant. (Wrong Content-Type)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        return await super().fetch_token(OAUTH_LOGIN_ENDPOINT, code=None, authorization_response=None,
                                         body='', auth=None, username=username, password=password, method='POST',
                                         timeout=None, headers=headers, verify_ssl=True,
                                         post_payload_modifier=json.dumps)

    async def refresh_token(self, token_url, **kwargs):  # pylint: disable=arguments-differ
        # Note, Snoo OAuth API is not 100% RFC 6749 compliant. (Wrong Content-Type)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        return await super().refresh_token(token_url, headers=headers, post_payload_modifier=json.dumps, **kwargs)
