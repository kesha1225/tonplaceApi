"""
Пример получения токена
"""
import asyncio

from tonplace import get_token


async def main():
    token = await get_token("+79123456789", save_session=True)
    print(token)


asyncio.get_event_loop().run_until_complete(main())
