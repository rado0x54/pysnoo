#!/usr/bin/env python
"""Command line tool for interacting with the Snoo Bassinet API"""
import asyncio
import logging
import argparse
import getpass
import json
from pprint import pprint

from typing import Callable
from datetime import datetime, timedelta

from pysnoo import SnooAuthSession, Snoo, SnooPubNub
from pysnoo.models import dt_str_to_dt

logging.basicConfig(level=logging.DEBUG)

async def user(snoo: Snoo, args={}):
    user = await snoo.get_me()
    pprint(user.to_dict())

async def device(snoo: Snoo, args={}):
    devices = await snoo.get_devices()
    if (len(devices) > 0):
        pprint(devices[0].to_dict())

async def baby(snoo: Snoo, args={}):
    baby = await snoo.get_baby()
    pprint(baby.to_dict())

async def last_session(snoo: Snoo, args={}):
    last_session = await snoo.get_last_session()
    pprint(last_session.to_dict())

async def status(snoo: Snoo, args={}):
    last_session = await snoo.get_last_session()
    print(f'{last_session.current_status.value} (since: {last_session.current_status_duration})')

async def session(snoo: Snoo, args={}):
    session = await snoo.get_aggregated_session(args.datetime)
    pprint(session.to_dict())

async def session_avg(snoo: Snoo, args={}):
    baby = await snoo.get_baby()
    session_avg = await snoo.get_aggregated_session_avg(baby.baby, args.datetime)
    pprint(session_avg.to_dict())

async def total(snoo: Snoo, args={}):
    baby = await snoo.get_baby()
    total = await snoo.get_session_total_time(baby.baby)
    print(total)

async def monitor(snoo: Snoo, args={}):
    # Also checks for valid token
    devices = await snoo.get_devices()
    if not devices:
        # No devices
        print('There is no Snoo connected to that account!')
        return

    access_token = snoo.auth.access_token
    print(access_token)
    pubnub = SnooPubNub(access_token, devices[0].serial_number)
    pubnub.subscribe()

    env = await pubnub.history()
    print(env)
    while True:
        await asyncio.sleep(1)
        print('Sleeping Some!')

    # await asyncio.sleep(8000)

# Function Dictionary
commands = {
    'user': user,
    'device': device,
    'baby': baby,
    'last_session': last_session,
    'status': status,
    'session': session,
    'session_avg': session_avg,
    'total': total,
    'monitor': monitor
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
        print('GETTING HERE!!!!!!!!!!!!!!!!')

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
                                            'session_avg', 'total', 'monitor']
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
    # asyncio.run(async_main(args.username, args.password, token, token_updater, args))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(args.username, args.password, token, token_updater, args))


if __name__ == "__main__":
    main()
