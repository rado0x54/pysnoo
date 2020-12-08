import asyncio
import logging

from pysnoo.auth_session import SnooAuthSession

logging.basicConfig(level=logging.DEBUG)


async def main():
    print('Hello ...')
    async with SnooAuthSession() as auth:
        token = await auth.fetch_token('USER', 'PASSWORD')
        print('Token: {}'.format(token))

        me_response = await auth.get('https://snoo-api.happiestbaby.com/us/me/')
        print('Me: {}'.format(me_response))


# Python 3.7+
asyncio.run(main())
