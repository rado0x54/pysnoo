"""TestClass for the Snoo Client"""
import json

from asynctest import TestCase, patch, CoroutineMock
from pysnoo.const import SNOO_ME_ENDPOINT
from pysnoo.auth_session import SnooAuthSession
from pysnoo.snoo import Snoo
from pysnoo import User

from tests.helpers import load_fixture, get_token


class TestSnooClient(TestCase):
    """Snoo Client Test class"""

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_user(self, mocked_request):
        """Test the successful GET /me endpoint"""
        # Setup
        token, _ = get_token()
        user_json = json.loads(load_fixture('', 'us_me__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[user_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            user = await snoo.get_me()

            # Check Request
            mocked_request.assert_called_once_with(
                'GET', SNOO_ME_ENDPOINT,
                data=None,
                allow_redirects=True,
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(user, User.from_dict(user_json))
