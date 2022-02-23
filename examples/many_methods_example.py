"""
Разные методы
"""
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

    res = await api.get_dialogs()
    print(res)

    res = await api.get_notify()
    print(res)

    res = await api.get_balance()
    print(res)

    res = await api.get_referrals()
    print(res)

    res = await api.edit_profile(
        birth_day=2,
        birth_month=3,
        birth_year=1990,
        city_id=0,
        country_id=0,
        first_name="test",
        last_name="test",
        sex=2,
    )
    print(res)

    res = await api.check_domain("durov")
    print(res)

    res = await api.change_domain("durov555")
    print(res)

    await api.close()


asyncio.get_event_loop().run_until_complete(main())
