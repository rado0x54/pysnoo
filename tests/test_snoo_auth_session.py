# -*- coding: utf-8 -*-
"""TestClass for the SnooAuthSession (and underlying OAuthBaseSession)"""
import json

from asynctest import TestCase, patch, CoroutineMock, ANY, MagicMock
from callee import Contains
from oauthlib.oauth2 import OAuth2Error

from pysnoo.const import (OAUTH_LOGIN_ENDPOINT,
                          OAUTH_TOKEN_REFRESH_ENDPOINT,
                          SNOO_API_URI,
                          BASE_HEADERS)
from pysnoo.auth_session import SnooAuthSession

from tests.helpers import load_fixture, get_token


class TestSnooAuthSession(TestCase):
    """SnooAuthSession Test class"""

    @patch('aiohttp.client.ClientSession._request')
    async def test_login_success(self, mocked_request):
        """Test the successful fetch of an initial token"""
        # Setup
        _, token_response = get_token()
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response])
        async with SnooAuthSession() as session:

            # Test
            await session.fetch_token('USER', 'PASSWORD')

            # Check
            mocked_request.assert_called_once_with(
                'POST', OAUTH_LOGIN_ENDPOINT,
                data=json.dumps({'grant_type': 'password', 'username': 'USER', 'password': 'PASSWORD'}),
                timeout=None,
                # Base Headers are only added in _request, which is mocked.
                headers={'Accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8'},
                auth=ANY,
                verify_ssl=True)

            self.assertEqual(session.headers, BASE_HEADERS)
            self.assertTrue(session.authorized)

    @patch('aiohttp.client.ClientSession._request')
    async def test_login_failure(self, mocked_request):
        """Test the failed fetch of an initial token"""
        token_response = load_fixture('', 'us_login__post_400.json')
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response])

        async with SnooAuthSession() as session:
            with self.assertRaises(OAuth2Error):
                await session.fetch_token('USER', 'WRONG_PASSWORD')

    @patch('aiohttp.client.ClientSession._request')
    async def test_refresh_expired_token(self, mocked_request):
        """Test the automatic refresh of an expired token"""
        token, token_response = get_token(-10)

        mocked_tocken_updater = MagicMock()

        # Token Refresh POST
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response, "test"])

        async with SnooAuthSession(token=token, token_updater=mocked_tocken_updater) as session:
            async with session.get(SNOO_API_URI) as resp:
                response_body = await resp.text()
                self.assertEqual('test', response_body)

        # Just make sure REFRESH CALL has the correct updated data and header attributes.
        mocked_request.assert_any_call(
            'POST', OAUTH_TOKEN_REFRESH_ENDPOINT,
            data=json.dumps({'grant_type': 'refresh_token',
                             'refresh_token': token['refresh_token'],
                             'allow_redirects': 'True'}),
            timeout=None,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8'},
            auth=None,
            verify_ssl=True)

        # Check that token_updater function was called with new TOKEN
        mocked_tocken_updater.assert_called_once_with(Contains('access_token'))
