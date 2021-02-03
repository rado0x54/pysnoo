#!/usr/bin/env python
"""Command line tool for interacting with the Snoo Bassinet API"""
import asyncio
import logging
import argparse
import getpass
import json
from pprint import pprint

from typing import Callable
from datetime import datetime

from pysnoo import SnooAuthSession, Snoo

# logging.basicConfig(level=logging.DEBUG)

async def user(snoo: Snoo):
    user = await snoo.get_me()
    pprint(user.to_dict())

async def device(snoo: Snoo):
    devices = await snoo.get_devices()
    if (len(devices) > 0):
        pprint(devices[0].to_dict())

async def baby(snoo: Snoo):
    baby = await snoo.get_baby()
    pprint(baby.to_dict())

async def last_session(snoo: Snoo):
    last_session = await snoo.get_last_session()
    pprint(last_session.to_dict())

async def status(snoo: Snoo):
    last_session = await snoo.get_last_session()
    print(f'{last_session.current_status.value} (since: {last_session.current_status_duration})')

async def session(snoo: Snoo):
    session = await snoo.get_aggregated_session(datetime(2021,2,2,7,0,0))
    pprint(session.to_dict())

# Function Dictionary
functions = {
    'user': user,
    'device': device,
    'baby': baby,
    'last_session': last_session,
    'status': status,
    'session': session
}

async def async_main(username, password, token, token_updater, func: Callable[[Snoo], None]):
    """Async Main"""

    async with SnooAuthSession(token, token_updater) as auth:

        if not auth.authorized:
            # Init Auth
            new_token = await auth.fetch_token(username, password)
            token_updater(new_token)

        snoo = Snoo(auth)
        await func(snoo)

        # baby = await snoo.set_baby_info('John 3', date(2021, 1, 18), 6, None)
        # print(f'{baby}')
        # # aggregated_session = await snoo.get_aggregated_session(datetime(2021, 2, 2, 7, 0, 0))
        # # print(f'{aggregated_session}')
        # aggregated_session = await snoo.get_aggregated_session(datetime(2021, 2, 2, 13, 30, 0))
        # print(f'{aggregated_session}')
        # aggregated_session_avg = await snoo.get_aggregated_session_avg(baby.baby, datetime(2021, 1, 21, 0, 0, 0))
        # print(f'{aggregated_session_avg}')
        # aggregated_session_avg = await snoo.get_aggregated_session_avg(baby.baby,
        #                                                                datetime(2021, 1, 21, 0, 0, 0), days=False)
        # print(f'{aggregated_session_avg}')
        # total_time = await snoo.get_session_total_time(baby.baby)
        # print(f'{total_time}')

        # async with auth.get(SNOO_BABY_ENDPOINT) as response:
        #     json_body = await response.json()
        #     print(json_body)


        # async with auth.get("https://httpbin.org/headers") as r:
        #     json_body = await r.json()
        #     print(json_body)

        # pubnub = SnooPubNub(auth.access_token, SERIAL)
        # pubnub.subscribe()


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


def _header():
    _bar()
    print("Snoo CLI")
    _bar()


def _bar():
    print('---------------------------------')


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
        'command', default='user', choices=['user', 'device', 'baby', 'last_session', 'status', 'session']
    )

    parser.add_argument('-u',
                        '--username',
                        dest='username',
                        type=str,
                        help='username for Snoo account')

    parser.add_argument('-p',
                        '--password',
                        type=str,
                        dest='password',
                        help='username for Snoo account')

    parser.add_argument('-t',
                        '--tokenFile',
                        metavar='file',
                        default='.snoo_token.txt',
                        dest='token_file',
                        help='Cached token file to read and write an existing OAuth Token to.')

    args = parser.parse_args()
    _header()

    token = get_token(args.token_file)

    if not token and not args.username:
        args.username = get_username()

    if not token and not args.password:
        args.password = getpass.getpass("Password: ")

    token_updater = get_token_updater(args.token_file)

    # Python 3.7+
    asyncio.run(async_main(args.username, args.password, token, token_updater, functions[args.command]))


if __name__ == "__main__":
    main()
