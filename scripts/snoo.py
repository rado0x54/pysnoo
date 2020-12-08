import asyncio
import logging
import argparse

from pysnoo.auth_session import SnooAuthSession

logging.basicConfig(level=logging.DEBUG)


async def async_main(username, password, token):
    print('Hello ...')
    async with SnooAuthSession() as auth:
        new_token = await auth.fetch_token(username, password)
        print('Token: {}'.format(new_token))

        me_response = await auth.get('https://snoo-api.happiestbaby.com/us/me/')
        print('Me: {}'.format(await me_response.json()))


def _header():
    _bar()
    print("Snoo CLI")
    _bar()


def _bar():
    print('---------------------------------')


def get_username():
    """read username from STDIN"""
    try:
        username = raw_input("Username: ")
    except NameError:
        username = input("Username: ")
    return username


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
                    '--token',
                    type=str,
                    dest='token',
                    help='existing token for the Snoo account')

args = parser.parse_args()
_header()

if not args.username:
    args.username = get_username()

if not args.password:
    args.password = getpass.getpass("Password: ")

# Python 3.7+
asyncio.run(async_main(args.username, args.password, args.token))
