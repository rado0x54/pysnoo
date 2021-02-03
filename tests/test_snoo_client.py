"""TestClass for the Snoo Client"""
import json
from datetime import date, datetime

from asynctest import TestCase, patch, CoroutineMock
from pysnoo.const import (SNOO_ME_ENDPOINT, SNOO_DEVICES_ENDPOINT, SNOO_BABY_ENDPOINT,
                          SNOO_SESSIONS_LAST_ENDPOINT,
                          SNOO_SESSIONS_AGGREGATED_ENDPOINT)
from pysnoo import (SnooAuthSession, Snoo,
                    MinimalLevel,
                    MinimalLevelVolume,
                    ResponsivenessLevel,
                    SoothingLevelVolume,
                    User, Device, Baby, Sex,
                    LastSession,
                    AggregatedSession)

from tests.helpers import load_fixture, get_token


class TestSnooClient(TestCase):
    """Snoo Client Test class"""

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_user(self, mocked_request):
        """Test the successful GET /us/me endpoint"""
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

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_devices(self, mocked_request):
        """Test the successful GET /ds/me/devices endpoint"""
        # Setup
        token, _ = get_token()
        devices_json = json.loads(load_fixture('', 'ds_me_devices__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[devices_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            devices = await snoo.get_devices()

            # Check Request
            mocked_request.assert_called_once_with(
                'GET', SNOO_DEVICES_ENDPOINT,
                data=None,
                allow_redirects=True,
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(devices, [Device.from_dict(devices_json[0])])

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_last_session(self, mocked_request):
        """Test the successful GET /ss/v2/sessions/last endpoint"""
        # Setup
        token, _ = get_token()
        last_session_json = json.loads(load_fixture('', 'ss_v2_sessions_last__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[last_session_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            last_session = await snoo.get_last_session()

            # Check Request
            mocked_request.assert_called_once_with(
                'GET', SNOO_SESSIONS_LAST_ENDPOINT,
                data=None,
                allow_redirects=True,
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(last_session, LastSession.from_dict(last_session_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_aggregated_session(self, mocked_request):
        """Test the successful GET /ss/v2/sessions/aggregated endpoint"""
        # Setup
        token, _ = get_token()
        aggregated_session_json = json.loads(load_fixture('', 'ss_v2_sessions_aggregated__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[aggregated_session_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            aggregated_session = await snoo.get_aggregated_session(datetime(2021, 2, 2, 7, 30, 45, 123000))

            # Check Request
            mocked_request.assert_called_once_with(
                'GET', SNOO_SESSIONS_AGGREGATED_ENDPOINT,
                data=None,
                allow_redirects=True,
                params={'startTime': '2021-02-02 07:30:45.123'},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(aggregated_session, AggregatedSession.from_dict(aggregated_session_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_get_baby(self, mocked_request):
        """Test the successful GET /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.get_baby()

            # Check Request
            mocked_request.assert_called_once_with(
                'GET', SNOO_BABY_ENDPOINT,
                data=None,
                allow_redirects=True,
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_baby_info(self, mocked_request):
        """Test the successful PATCH of baby info to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_baby_info('BABY_NAME', date(2021, 12, 5), 5, Sex.FEMALE)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'babyName': 'BABY_NAME', 'birthDate': '2021-12-05', 'preemie': 5, 'sex': 'Female'},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_minimal_level(self, mocked_request):
        """Test the successful PATCH of minimal_level setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_minimal_level(MinimalLevel.LEVEL1)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'minimalLevel': 'level1'}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_minimal_level_volume(self, mocked_request):
        """Test the successful PATCH of minimal_level_volume setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_minimal_level_volume(MinimalLevelVolume.VERY_LOW)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'minimalLevelVolume': 'lvl-2'}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_responsiveness_level(self, mocked_request):
        """Test the successful PATCH of responsiveness_level setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_responsiveness_level(ResponsivenessLevel.VERY_HIGH)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'responsivenessLevel': 'lvl+2'}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_soothing_level_volume(self, mocked_request):
        """Test the successful PATCH of soothing_level_volume setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_soothing_level_volume(SoothingLevelVolume.NORMAL)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'soothingLevelVolume': 'lvl0'}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_motion_limiter(self, mocked_request):
        """Test the successful PATCH of motion_limiter setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_motion_limiter(False)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'motionLimiter': False}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))

    @patch('aiohttp.client.ClientSession._request')
    async def test_set_weaning(self, mocked_request):
        """Test the successful PATCH of weaning setting to /us/v3/me/baby endpoint"""
        # Setup
        token, _ = get_token()
        baby_json = json.loads(load_fixture('', 'us_v3_me_baby__get_200.json'))
        mocked_request.return_value.json = CoroutineMock(side_effect=[baby_json])
        mocked_request.return_value.status = 200

        async with SnooAuthSession(token) as session:
            snoo = Snoo(session)
            # Test
            baby = await snoo.set_weaning(True)

            # Check Request
            mocked_request.assert_called_once_with(
                'PATCH', SNOO_BABY_ENDPOINT,
                data=None,
                json={'settings': {'weaning': True}},
                # Base Headers are only added in _request, which is mocked.
                headers={'Authorization': 'Bearer {}'.format(token['access_token'])})

            # Check Response
            self.assertEqual(baby, Baby.from_dict(baby_json))
