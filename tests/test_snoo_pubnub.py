"""TestClass for the Snoo Pubnub"""
import json

from pubnub.enums import PNOperationType, PNStatusCategory
from pubnub.callbacks import SubscribeCallback
from pubnub.models.consumer.common import PNStatus
from pubnub.models.consumer.pubsub import PNMessageResult

from asynctest import TestCase, patch, MagicMock
from pysnoo import SnooPubNub, SessionLevel, ActivityState
from pysnoo.const import SNOO_PUBNUB_PUBLISH_KEY, SNOO_PUBNUB_SUBSCRIBE_KEY

from tests.helpers import load_fixture


class TestSnooPubnub(TestCase):
    """Snoo Client PubNub class"""

    def setUp(self):
        self.pubnub = SnooPubNub('ACCESS_TOKEN',
                                 'SERIAL_NUMBER',
                                 'UUID',
                                 MagicMock(),
                                 custom_event_loop=self.loop)

    async def tearDown(self):
        # pylint: disable=invalid-overridden-method
        if self.pubnub:
            await self.pubnub.stop()

    @patch('pubnub.pubnub_asyncio.PubNubAsyncio.request_future')
    async def test_publish_start(self, mocked_request):
        """Test publish_start"""
        # pylint: disable=protected-access
        # Setup
        await self.pubnub.publish_start()

        mocked_request.assert_called_once()
        self.assertIsNone(mocked_request.mock_calls[0][2]['cancellation_event'])
        options = mocked_request.mock_calls[0][2]['options_func']()
        self.assertEqual(options.path, f'/publish/{SNOO_PUBNUB_PUBLISH_KEY}/{SNOO_PUBNUB_SUBSCRIBE_KEY}/0/'
                                       f'ControlCommand.SERIAL_NUMBER/0/%7B%22command%22%3A%20%22start_snoo%22%7D')
        self.assertEqual(options.operation_type, PNOperationType.PNPublishOperation)
        self.assertIsNone(options.data)
        self.assertEqual(options.method_string, 'GET')
        # This needs to be called to retrieve the params from the configuration
        options.merge_params_in({})
        self.assertEqual(options.query_string,
                         f'auth=ACCESS_TOKEN&pnsdk=PubNub-Python-Asyncio%2F{self.pubnub._pubnub.SDK_VERSION}&uuid=UUID')

    @patch('pubnub.pubnub_asyncio.PubNubAsyncio.request_future')
    async def test_publish_goto_state(self, mocked_request):
        """Test publish_goto_state"""
        # pylint: disable=protected-access
        # Setup
        await self.pubnub.publish_goto_state(SessionLevel.LEVEL1)

        mocked_request.assert_called_once()
        self.assertIsNone(mocked_request.mock_calls[0][2]['cancellation_event'])
        options = mocked_request.mock_calls[0][2]['options_func']()
        self.assertEqual(options.path, f'/publish/{SNOO_PUBNUB_PUBLISH_KEY}/{SNOO_PUBNUB_SUBSCRIBE_KEY}/0/'
                                       f'ControlCommand.SERIAL_NUMBER/0/'
                                       f'%7B%22command%22%3A%20%22go_to_state%22%2C%20%22state%22%3A%20%22LEVEL1%22%7D')
        self.assertEqual(options.operation_type, PNOperationType.PNPublishOperation)
        self.assertIsNone(options.data)
        self.assertEqual(options.method_string, 'GET')
        # This needs to be called to retrieve the params from the configuration
        options.merge_params_in({})
        self.assertEqual(options.query_string,
                         f'auth=ACCESS_TOKEN&pnsdk=PubNub-Python-Asyncio%2F{self.pubnub._pubnub.SDK_VERSION}&uuid=UUID')

    @patch('pubnub.pubnub_asyncio.PubNubAsyncio.request_future')
    async def test_publish_goto_state_with_hold(self, mocked_request):
        """Test publish_goto_state with hold parameter"""
        # pylint: disable=protected-access
        # Setup
        await self.pubnub.publish_goto_state(SessionLevel.LEVEL2, hold=False)

        mocked_request.assert_called_once()
        self.assertIsNone(mocked_request.mock_calls[0][2]['cancellation_event'])
        options = mocked_request.mock_calls[0][2]['options_func']()
        self.assertEqual(options.path, f'/publish/{SNOO_PUBNUB_PUBLISH_KEY}/{SNOO_PUBNUB_SUBSCRIBE_KEY}/0/'
                                       f'ControlCommand.SERIAL_NUMBER/0/'
                                       f'%7B%22command%22%3A%20%22go_to_state%22%2C%20%22state%22%3A%20%22LEVEL2'
                                       f'%22%2C%20%22hold%22%3A%20%22off%22%7D')
        self.assertEqual(options.operation_type, PNOperationType.PNPublishOperation)
        self.assertIsNone(options.data)
        self.assertEqual(options.method_string, 'GET')
        # This needs to be called to retrieve the params from the configuration
        options.merge_params_in({})
        self.assertEqual(options.query_string,
                         f'auth=ACCESS_TOKEN&pnsdk=PubNub-Python-Asyncio%2F{self.pubnub._pubnub.SDK_VERSION}&uuid=UUID')

    @patch('pubnub.pubnub_core.PubNubCore.add_listener')
    @patch('pubnub.managers.SubscriptionManager.adapt_subscribe_builder')
    async def test_subscribe(self, mocked_subscribe_builder, mocked_add_listener):
        """Test subscribe"""
        # Setup

        def add_listener_side_effect(listener: SubscribeCallback):
            # Call Connect Status.
            pn_status = PNStatus()
            pn_status.category = PNStatusCategory.PNConnectedCategory
            # Call after 1s: listener.status(self.pubnub._pubnub, pn_status)
            self.loop.call_later(1, listener.status, self.pubnub._pubnub, pn_status)  # pylint: disable=protected-access

        mocked_add_listener.side_effect = add_listener_side_effect

        await self.pubnub.subscribe()

        mocked_add_listener.assert_called_once()
        mocked_subscribe_builder.assert_called_once()
        subscribe_operation = mocked_subscribe_builder.mock_calls[0][1][0]
        self.assertEqual(subscribe_operation.channels, ['ActivityState.SERIAL_NUMBER'])
        self.assertEqual(subscribe_operation.channel_groups, [])
        self.assertEqual(subscribe_operation.presence_enabled, False)
        self.assertEqual(subscribe_operation.timetoken, 0)

    @patch('pubnub.managers.SubscriptionManager.adapt_unsubscribe_builder')
    async def test_unsubscribe(self, mocked_unsubscribe_builder):
        """Test unsubscribe"""
        # pylint: disable=protected-access
        # Call Connect Status.
        pn_status = PNStatus()
        pn_status.category = PNStatusCategory.PNAcknowledgmentCategory
        pn_status.operation = PNOperationType.PNUnsubscribeOperation
        # Call after 1s: listener.status(self.pubnub._pubnub, pn_status)
        self.loop.call_later(1, self.pubnub._listener.status, self.pubnub._pubnub, pn_status)

        await self.pubnub.unsubscribe()

        mocked_unsubscribe_builder.assert_called_once()
        unsubscribe_operation = mocked_unsubscribe_builder.mock_calls[0][1][0]
        self.assertEqual(unsubscribe_operation.channels, ['ActivityState.SERIAL_NUMBER'])
        self.assertEqual(unsubscribe_operation.channel_groups, [])

    @patch('pubnub.pubnub_asyncio.PubNubAsyncio.request_future')
    async def test_history(self, mocked_request):
        """Test history"""
        # pylint: disable=protected-access

        count = 55
        await self.pubnub.history(count)

        mocked_request.assert_called_once()
        self.assertIsNone(mocked_request.mock_calls[0][2]['cancellation_event'])
        options = mocked_request.mock_calls[0][2]['options_func']()
        self.assertEqual(options.path, f'/v2/history/sub-key/{SNOO_PUBNUB_SUBSCRIBE_KEY}/channel/'
                                       f'ActivityState.SERIAL_NUMBER')
        self.assertEqual(options.operation_type, PNOperationType.PNHistoryOperation)
        self.assertIsNone(options.data)
        self.assertEqual(options.method_string, 'GET')
        # This needs to be called to retrieve the params from the configuration
        options.merge_params_in({})
        self.assertEqual(
            options.query_string, f'count={count}&pnsdk=PubNub-Python-Asyncio%2F{self.pubnub._pubnub.SDK_VERSION}&'
                                  f'uuid=UUID&auth=ACCESS_TOKEN')

    async def test_message_callback(self):
        """Test listener Callback on Message"""
        # pylint: disable=protected-access
        activity_state_msg_payload = json.loads(
            load_fixture('', 'pubnub_message_ActivityState.json'))
        activity_state = ActivityState.from_dict(activity_state_msg_payload)

        callback = self.pubnub._listener._callback

        self.pubnub._listener.message(self.pubnub._pubnub, PNMessageResult(
            activity_state_msg_payload, None, None, 0))

        callback.assert_called_once_with(activity_state)
