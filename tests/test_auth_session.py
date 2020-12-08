from asynctest import TestCase, patch, CoroutineMock, ANY, MagicMock, call
from callee import Contains
import json
from oauthlib.oauth2 import OAuth2Error

from pysnoo.const import OAuth, SNOO_API_URI
from pysnoo.auth_session import SnooAuthSession

from tests.helpers import load_fixture


class TestSnooAuthSession(TestCase):
    """SnooAuthSession Test class"""

    @patch('aiohttp.client.ClientSession._request')
    async def test_login_success(self, mocked_request):
        # Setup
        token_response = load_fixture('', 'access_token_response.json')
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response])
        async with SnooAuthSession() as session:

            # Test
            resp = await session.fetch_token('USER', 'PASSWORD')

            # Check
            mocked_request.assert_called_once_with(
                'POST', OAuth.LOGIN_ENDPOINT,
                json={'grant_type': 'password', 'username': 'USER', 'password': 'PASSWORD'},
                data=None,
                timeout=None,
                headers={'Accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8'},
                auth=ANY,
                verify_ssl=True)

            token_json = json.loads(token_response)
            token_json['scope'] = token_json['scope'].split(' ')
            self.assertDictContainsSubset(token_json, resp)

    @patch('aiohttp.client.ClientSession._request')
    async def test_login_failure(self, mocked_request):
        token_response = load_fixture('', 'login_400.json')
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response])

        async with SnooAuthSession() as session:
            with self.assertRaises(OAuth2Error):
                await session.fetch_token('USER', 'WRONG_PASSWORD')

    @patch('aiohttp.client.ClientSession._request')
    async def test_refresh_expired_token(self, mocked_request):
        # loop = asyncio.get_event_loop()
        token_response = load_fixture('', 'access_token_response.json')
        token_response_dict = json.loads(token_response)
        token_response_dict['expires_in'] = -10

        mocked_tocken_updater = MagicMock()

        # Token Refresh POST
        mocked_request.return_value.text = CoroutineMock(side_effect=[token_response, "test"])

        async with SnooAuthSession(token=token_response_dict, token_updater=mocked_tocken_updater) as session:
            self.assertIsNotNone(session)
            async with session.get(SNOO_API_URI) as resp:
                self.assertIsNotNone(resp)
                response_body = await resp.text()
                self.assertEqual('test', response_body)

        # Check that TOKEN_REFRESH_ENDPOINT was called
        mocked_request.assert_has_calls([
            call('POST', OAuth.TOKEN_REFRESH_ENDPOINT,
                 json={'grant_type': 'refresh_token', 'refresh_token': token_response_dict['refresh_token'], 'allow_redirects': 'True'},
                 data=None,
                 timeout=None,
                 headers={'Accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8'},
                 auth=None,
                 verify_ssl=True),
            call().text(),
            call().release(),
            call('GET', SNOO_API_URI,
                 headers={'Authorization': 'Bearer {}'.format(token_response_dict['access_token'])},
                 data=None,
                 allow_redirects=True),
            call().text(),
            call().release()])

        # Check that token_updater function was called with new TOKEN
        mocked_tocken_updater.assert_called_once_with(Contains('access_token'))






