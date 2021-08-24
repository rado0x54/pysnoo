"""PySnoo PubNub Interface."""
import asyncio
import logging
from typing import Callable, Optional, List
from dataclasses import dataclass
from aiohttp.connector import Connection

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration, PNReconnectionPolicy
from pubnub.pubnub_asyncio import PubNubAsyncio, utils
from pubnub.enums import PNStatusCategory

from .models import ActivityState, SessionLevel
from .const import SNOO_PUBNUB_PUBLISH_KEY, SNOO_PUBNUB_SUBSCRIBE_KEY, OAUTH_TOKEN_REFRESH_ENDPOINT
from . import SnooAuthSession

_LOGGER = logging.getLogger(__name__)

@dataclass(frozen=True)
class ConnectionState:
    """SnooPubNub connection state."""

    is_connected: bool
    token_refresh_required: bool

class SnooSubscribeListener(SubscribeCallback):
    """Snoo Subscription Listener Class"""

    def __init__(self, activity_state_callback: Callable[[ActivityState], None], connection_callback: Callable[[ConnectionState], None]):
        """Initialize the Snoo Subscription Listener"""
        self.connected_event = asyncio.Event()
        self.disconnected_event = asyncio.Event()
        self._activity_state_callback = activity_state_callback
        self._connection_callback = connection_callback

    def status(self, pubnub, status):
        """PubNub Status Callback Implementation"""
        token_refresh_required = False
        was_connected = self.connected_event.is_set()
        is_connected = was_connected
        if status.category == PNStatusCategory.PNConnectedCategory or \
           status.category == PNStatusCategory.PNReconnectedCategory:
            is_connected = True
        elif status.category == PNStatusCategory.PNAccessDeniedCategory:
            _LOGGER.debug("Disconnected (Access Denied)!")
            token_refresh_required = True
            is_connected = False
        elif utils.is_unsubscribed_event(status):
            is_connected = False
        elif status.is_error():
            _LOGGER.warn('Error in Snoo PubNub Listener of Category: %s', status.category)

        if is_connected and not was_connected:
            _LOGGER.debug("Connected! (Category %s)", status.category)
            self.connected_event.set()
            self.disconnected_event.clear()
        if not is_connected and was_connected:
            _LOGGER.debug("Disconnected! (Category %s)", status.category)
            self.disconnected_event.set()
            self.connected_event.clear()
        
        if is_connected != was_connected:
            self._connection_callback(ConnectionState(
                is_connected=is_connected,
                token_refresh_required=token_refresh_required
            ))

    def message(self, pubnub, message):
        """PubNub Message Callback Implementation"""
        self._activity_state_callback(ActivityState.from_dict(message.message))

    def presence(self, pubnub, presence):
        """PubNub Presence Callback Implementation"""

    def is_connected(self):
        """Returns true if the listener is currently connected to an active subscription"""
        return self.connected_event.is_set()

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
                 auth: SnooAuthSession,
                 serial_number: str,
                 uuid: str,
                 custom_event_loop=None):
        """Initialize the Snoo PubNub object."""
        self.config = self._setup_pnconfig(auth, uuid)
        self.serial_number = serial_number
        self._auth = auth
        self._activity_channel = 'ActivityState.{}'.format(serial_number)
        self._controlcommand_channel = 'ControlCommand.{}'.format(serial_number)
        self._pubnub = PubNubAsyncio(self.config, custom_event_loop=custom_event_loop)
        self._listener = SnooSubscribeListener(self._activity_state_callback, self._connection_callback)
        # Add listener
        self._pubnub.add_listener(self._listener)
        self._external_listeners: List[Callable[[ActivityState], None]] = []
        self._connection_listeners: List[Callable[[bool], None]] = []

    @staticmethod
    def _setup_pnconfig(auth, uuid):
        """Generate Setup"""
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = SNOO_PUBNUB_SUBSCRIBE_KEY
        pnconfig.publish_key = SNOO_PUBNUB_PUBLISH_KEY
        pnconfig.uuid = uuid
        pnconfig.auth_key = auth.access_token
        pnconfig.ssl = True
        pnconfig.reconnect_policy = PNReconnectionPolicy.EXPONENTIAL
        return pnconfig

    def add_listener(self, update_callback: Callable[[ActivityState], None]) -> Callable[[], None]:
        """Add a ActivityState Listener to the SnooPubNub Entity and returns a remove_listener CB for that listener"""
        self._external_listeners.append(update_callback)

        def remove_listener_cb() -> None:
            """Remove listener."""
            self.remove_listener(update_callback)

        return remove_listener_cb

    def remove_listener(self, update_callback: Callable[[ActivityState], None]) -> None:
        """Remove data update."""
        self._external_listeners.remove(update_callback)

    def add_connection_listener(self, update_callback: Callable[[bool], None]) -> Callable[[], None]:
        """Add a connection Listener to the SnooPubNub Entity and returns a remove_connection_listener CB for that listener"""
        self._connection_listeners.append(update_callback)

        def remove_listener_cb() -> None:
            """Remove listener."""
            self.remove_connection_listener(update_callback)

        return remove_listener_cb

    def remove_connection_listener(self, update_callback: Callable[[bool], None]) -> None:
        """Remove connection update."""
        self._connection_listeners.remove(update_callback)

    def _activity_state_callback(self, state: ActivityState):
        """Internal Callback of SnooSubscribeListener"""
        for update_callback in self._external_listeners:
            update_callback(state)

    def _connection_callback(self, connection: ConnectionState):
        """Internal Callback of SnooSubscribeListener"""
        if connection.token_refresh_required:
            asyncio.create_task(self._refresh_token())

        for update_callback in self._connection_listeners:
            update_callback(connection.is_connected)
    
    async def _refresh_token(self):
        """Refresh the Snoo token to allow PubNub to reconnect"""
        await self._auth.refresh_token(OAUTH_TOKEN_REFRESH_ENDPOINT)
        self.config.auth_key = self._auth.access_token

    def is_connected(self):
        """Return if PubNub is connected"""
        return self._listener.is_connected()

    def subscribe(self):
        """Subscribe to Snoo Activity Channel"""
        if self._listener.is_connected():
            _LOGGER.warning('Trying to subscribe PubNub instance that is already subscribed to %s',
                            self._activity_channel)
            return

        self._pubnub.subscribe().channels([
            self._activity_channel
        ]).execute()

    async def subscribe_and_await_connect(self):
        """Subscribe to Snoo Activity Channel and await connect"""
        self.subscribe()
        await self._listener.wait_for_connect()

    def unsubscribe(self):
        """Unsubscribe to Snoo Activity Channel"""
        if not self._listener.is_connected():
            _LOGGER.warning('Trying to unsubscribe PubNub instance that is NOT subscribed to %s', self._activity_channel)
            return

        self._pubnub.unsubscribe().channels(
            self._activity_channel
        ).execute()

    async def unsubscribe_and_await_disconnect(self):
        """Unsubscribe to Snoo Activity Channel and await disconnect"""
        self.unsubscribe()
        await self._listener.wait_for_disconnect()

    async def history(self, count=1):
        """Retrieve number of count historic messages"""
        envelope = await self._pubnub.history().channel(
            self._activity_channel
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
