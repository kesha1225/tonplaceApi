import asyncio

from tonplace import get_token, API


async def main():
    token = await get_token("+79123456789", save_session=True)
    api = API(token)

    res = await api.read_post(512259)
    print(res)

    res = await api.read_posts([512259, 512446])
    print(res)

    res = await api.get_post(512259)
    print(res)

    res = await api.get_feed("liked")
    print(res)

    await api.close()


asyncio.get_event_loop().run_until_complete(main())
