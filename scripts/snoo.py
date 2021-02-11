#!/usr/bin/env python
"""Command line tool for interacting with the Snoo Bassinet API"""
import asyncio
import argparse
import getpass
import json
from pprint import pprint

from datetime import datetime, timedelta
from pysnoo import SnooAuthSession, Snoo, SnooPubNub, SessionLevel
from pysnoo.models import dt_str_to_dt


async def _setup_pubnub(snoo: Snoo, callback):
    # Also checks for valid token
    devices = await snoo.get_devices()
    if not devices:
        # No devices
        print('There is no Snoo connected to that account!')
        return

    return SnooPubNub(snoo.auth.access_token,
                        devices[0].serial_number,
                        f'pn-pysnoo-{devices[0].serial_number}',
                        callback)

async def user(snoo: Snoo, args):
    resonse = await snoo.get_me()
    pprint(resonse.to_dict())

async def device(snoo: Snoo, args):
    devices = await snoo.get_devices()
    if len(devices) > 0:
        pprint(devices[0].to_dict())

async def baby(snoo: Snoo, args):
    baby = await snoo.get_baby()
    pprint(baby.to_dict())

async def last_session(snoo: Snoo, args):
    last_session = await snoo.get_last_session()
    pprint(last_session.to_dict())

async def status(snoo: Snoo, args):
    last_session = await snoo.get_last_session()
    print(f'{last_session.current_status.value} (since: {last_session.current_status_duration})')

async def session(snoo: Snoo, args):
    session = await snoo.get_aggregated_session(args.datetime)
    pprint(session.to_dict())

async def session_avg(snoo: Snoo, args):
    baby = await snoo.get_baby()
    session_avg = await snoo.get_aggregated_session_avg(baby.baby, args.datetime)
    pprint(session_avg.to_dict())

async def total(snoo: Snoo, args):
    baby = await snoo.get_baby()
    total = await snoo.get_session_total_time(baby.baby)
    print(total)

async def monitor(snoo: Snoo, args):
    def cb(msg):
        print(msg)

    pubnub = await _setup_pubnub(snoo, cb)

    for msg in await pubnub.history():
        cb(msg)

    await pubnub.subscribe()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await pubnub.unsubscribe()
        await pubnub.stop()


async def history(snoo: Snoo, args):
    pubnub = await _setup_pubnub(snoo, None)

    for msg in await pubnub.history(100):
        print(msg)

    await pubnub.stop()

async def toggle(snoo: Snoo, args):
    pubnub = await _setup_pubnub(snoo, None)

    lastActivityState = (await pubnub.history())[0]
    if lastActivityState.state_machine.state == SessionLevel.ONLINE:
        # Start
        await pubnub.publish_start()
    else:
        # Stop
        await pubnub.publish_goto_state(SessionLevel.ONLINE)

    await pubnub.stop()


async def toggleHold(snoo: Snoo, args):
    pubnub = await _setup_pubnub(snoo, None)

    lastActivityState = (await pubnub.history())[0]
    current_state = lastActivityState.state_machine.state
    current_hold = lastActivityState.state_machine.hold
    if current_state.is_active_level():
        # Toggle
        await pubnub.publish_goto_state(current_state, not current_hold)
    else:
        print('Cannot toggle hold when Snoo is not running!')

    await pubnub.stop()


async def up(snoo: Snoo, args):
    pubnub = await _setup_pubnub(snoo, None)

    lastActivityState = (await pubnub.history())[0]
    up_transition = lastActivityState.state_machine.up_transition
    if up_transition.is_active_level():
        # Toggle
        await pubnub.publish_goto_state(up_transition)
    else:
        print('No valid up-transition available!')

    await pubnub.stop()


async def down(snoo: Snoo):
    pubnub = await _setup_pubnub(snoo, None)

    last_activity_state = (await pubnub.history())[0]
    down_transition = last_activity_state.state_machine.down_transition
    if down_transition.is_active_level():
        # Toggle
        await pubnub.publish_goto_state(down_transition)
    else:
        print('No valid down-transition available!')

    await pubnub.stop()


# Commands dictionary
commands = {
    'user': user,
    'device': device,
    'baby': baby,
    'last_session': last_session,
    'status': status,
    'session': session,
    'session_avg': session_avg,
    'total': total,
    'monitor': monitor,
    'history': history,
    'toggle': toggle,
    'toggleHold': toggleHold,
    'up': up,
    'down': down,
}


async def async_main(username, password, token, token_updater, args: any):
    """Async Main"""

    async with SnooAuthSession(token, token_updater) as auth:

        if not auth.authorized:
            # Init Auth
            new_token = await auth.fetch_token(username, password)
            token_updater(new_token)

        snoo = Snoo(auth)
        await commands[args.command](snoo, args)


def get_token_updater(token_file):
    """Return an token_updater function writing tokens to token_file"""
    def token_updater(token):
        with open(token_file, 'w') as outfile:
            json.dump(token, outfile)
    return token_updater


def get_token(token_file):
    """Read a token from a token_file (fails silently)"""
    try:
        with open(token_file) as infile:
            token = json.load(infile)
            return token
    except FileNotFoundError:
        pass
    except ValueError:
        pass


def get_username():
    """read username from STDIN"""
    username = input("Username: ")
    return username


def main():
    """Sync Main"""
    parser = argparse.ArgumentParser(
        description='Snoo Smart Bassinett',
        epilog='https://github.com/rado0x54/pysnoo',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'command', default='user', choices=['user', 'device', 'baby',
                                            'last_session', 'status', 'session',
                                            'session_avg', 'total', 'monitor',
                                            'history', 'toggle', 'toggleHold', 'up', 'down']
    )

    parser.add_argument('-u',
                        '--username',
                        type=str,
                        help='username for Snoo account')

    parser.add_argument('-p',
                        '--password',
                        type=str,
                        help='username for Snoo account')

    parser.add_argument('-t',
                        '--token_file',
                        metavar='file',
                        default='.snoo_token.txt',
                        help='Cached token file to read and write an existing OAuth Token to.')

    parser.add_argument('-d',
                        '--datetime',
                        default=datetime.now() - timedelta(1),  # 24h prior
                        type=dt_str_to_dt,
                        help='Datetime in ISO8601 fromat. Used for some commands.',
    )

    args = parser.parse_args()
    token = get_token(args.token_file)
    token_updater = get_token_updater(args.token_file)

    if not token and not args.username:
        args.username = get_username()

    if not token and not args.password:
        args.password = getpass.getpass("Password: ")

    # Python 3.7+
    try:
        asyncio.run(async_main(args.username, args.password, token, token_updater, args))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
