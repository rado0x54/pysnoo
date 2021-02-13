"""PySnoo PubNub Interface."""
import asyncio
import logging
from typing import Callable, Optional

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio, utils

from .models import ActivityState, SessionLevel
from .const import SNOO_PUBNUB_PUBLISH_KEY, SNOO_PUBNUB_SUBSCRIBE_KEY


class SnooSubscribeListener(SubscribeCallback):
    """Snoo Subscription Listener Class"""

    def __init__(self, callback: Callable[[ActivityState], None]):
        """Initialize the Snoo Subscription Listener"""
        self.connected_event = asyncio.Event()
        self.disconnected_event = asyncio.Event()
        self._callback = callback

    def status(self, pubnub, status):
        """PubNub Status Callback Implementation"""
        if utils.is_subscribed_event(status) and not self.connected_event.is_set():
            self.connected_event.set()
        elif utils.is_unsubscribed_event(status) and not self.disconnected_event.is_set():
            self.disconnected_event.set()
        elif status.is_error():
            logging.error('Error in Snoo PubNub Listener of Category: %s', status.category)

    def message(self, pubnub, message):
        """PubNub Message Callback Implementation"""
        self._callback(ActivityState.from_dict(message.message))

    def presence(self, pubnub, presence):
        """PubNub Presence Callback Implementation"""

    async def wait_for_connect(self):
        """Async utility function that waits for subscription connect."""
        if not self.connected_event.is_set():
            await self.connected_event.wait()

    async def wait_for_disconnect(self):
        """Async utility function that waits for subscription disconnect."""
        if not self.disconnected_event.is_set():
            await self.disconnected_event.wait()


class SnooPubNub:
    """A Python Abstraction for Snoos PubNub Interface."""
    # pylint: disable=too-few-public-methods,fixme

    def __init__(self,
                 access_token: str,
                 snoo_serial: str,
                 uuid: str,
                 callback: Callable[[ActivityState], None],
                 custom_event_loop=None):
        """Initialize the Snoo PubNub object."""
        # self._access_token = access_token
        # self._snoo_serial = snoo_serial
        self._activiy_channel = 'ActivityState.{}'.format(snoo_serial)
        self._controlcommand_channel = 'ControlCommand.{}'.format(snoo_serial)
        self._pnconfig = self._setup_pnconfig(access_token, uuid)
        self._pubnub = PubNubAsyncio(self._pnconfig, custom_event_loop=custom_event_loop)
        self._listener = SnooSubscribeListener(callback)

    @staticmethod
    def _setup_pnconfig(access_token, uuid):
        """Generate Setup"""
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = SNOO_PUBNUB_SUBSCRIBE_KEY
        pnconfig.publish_key = SNOO_PUBNUB_PUBLISH_KEY
        pnconfig.uuid = uuid
        pnconfig.auth_key = access_token
        pnconfig.ssl = True
        return pnconfig

    async def subscribe(self):
        """Subscribe to Snoo Activity Channel"""
        self._pubnub.add_listener(self._listener)
        self._pubnub.subscribe().channels([
            self._activiy_channel
        ]).execute()

        await self._listener.wait_for_connect()

    async def unsubscribe(self):
        """Unsubscribe to Snoo Activity Channel"""
        self._pubnub.unsubscribe().channels(
            self._activiy_channel
        ).execute()
        await self._listener.wait_for_disconnect()

    async def history(self, count=1):
        """Retrieve number of count historic messages"""
        envelope = await self._pubnub.history().channel(
            self._activiy_channel
        ).count(count).future()
        return [ActivityState.from_dict(item.entry) for item in envelope.result.messages]

    async def publish(self, message):
        """Publish a message to the Snoo control command channel"""
        task = await self._pubnub.publish().channel(
            self._controlcommand_channel).message(message).future()
        return task

    async def publish_goto_state(self, level: SessionLevel, hold: Optional[bool] = None):
        """Publish a message a go_to_state command to the Snoo control command channel"""
        msg = {
            'command': 'go_to_state',
            'state': level.value
        }
        if hold is not None:
            msg['hold'] = 'on' if hold else 'off'
        return await self.publish(msg)

    async def publish_start(self):
        """Publish a message a start_snoo command to the Snoo control command channel"""
        return await self.publish({
            'command': 'start_snoo'
        })

    async def stop(self):
        """Stop and Cleanup the Async Pubnub Utility"""
        # pylint: disable=protected-access
        # Workaround until PR is accepted:
        # https://github.com/pubnub/python/pull/99
        # self._pubnub.stop()
        await self._pubnub._session.close()
        if self._pubnub._subscription_manager is not None:
            self._pubnub._subscription_manager.stop()
