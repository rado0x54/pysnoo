# coding: utf-8
"""PySnoo PubNub Interface."""
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        print('presence')
        print(presence)
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        print('status')
        print(status)
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print('PNStatusCategory.PNUnexpectedDisconnectCategory')
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print('PNStatusCategory.PNConnectedCategory')
            # pubnub.publish().channel('my_channel').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print('PNStatusCategory.PNReconnectedCategory')
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print('PNStatusCategory.PNDecryptionErrorCategory')
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)


class SnooPubNub:
    """A Python Abstraction for Snoos PubNub Interface."""

    def __init__(self, access_token, snoo_serial):
        """Initialize the Snoo PubNub object."""
        self._access_token = access_token
        self._snoo_serial = snoo_serial
        self._pnconfig = self._setup_pnconfig(access_token)
        self._pubnub = PubNub(self._pnconfig)

    def _setup_pnconfig(self, access_token):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "sub-c-97bade2a-483d-11e6-8b3b-02ee2ddab7fe"
        pnconfig.publish_key = "pub-c-699074b0-7664-4be2-abf8-dcbb9b6cd2b"
        pnconfig.uuid = "UUID"  # TODO: Change
        pnconfig.auth_key = access_token
        pnconfig.ssl = True
        return pnconfig

    def subscribe(self):
        self._pubnub.add_listener(MySubscribeCallback())
        self._pubnub.subscribe().channels([
            'ActivityState.{}'.format(self._snoo_serial),
            'ControlCommand.{}-pnpres'.format(self._snoo_serial)
        ]).execute()

