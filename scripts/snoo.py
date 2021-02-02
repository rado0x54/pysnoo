"""Snoo CLI Tool"""
import asyncio
import logging
import argparse
import getpass
import json
from datetime import date

from pysnoo import SnooAuthSession, Snoo
from pysnoo.const import SNOO_BABY_ENDPOINT

logging.basicConfig(level=logging.DEBUG)


async def async_main(username, password, token, token_updater):
    """Async Main"""

    async with SnooAuthSession(token, token_updater) as auth:

        if not auth.authorized:
            # Init Auth
            new_token = await auth.fetch_token(username, password)
            token_updater(new_token)

        snoo = Snoo(auth)

        user = await snoo.get_me()
        print(f'{user}')
        devices = await snoo.get_devices()
        print(f'{devices}')
        baby = await snoo.get_baby()
        print(f'{baby}')
        baby = await snoo.set_baby_info('John 3', date(2021, 1, 18), 6, None)
        print(f'{baby}')

        async with auth.get(SNOO_BABY_ENDPOINT) as response:
            json_body = await response.json()
            print(json_body)


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
    asyncio.run(async_main(args.username, args.password, token, token_updater))


if __name__ == "__main__":
    main()
