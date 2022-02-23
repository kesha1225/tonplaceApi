"""
Парсинг новых пользователей
"""
import asyncio

from tonplace import get_token, API


async def main():
    token = await get_token("+79123456789")
    api = API(token)

    new_users = await api.search(tab="peoples", sort="new")
    for user_id, user_data in new_users["users"].items():
        print(user_data)

        user = await api.get_user(user_data["id"])
        # этот запрос возвращает данные которые уже есть в user_data, сделан просто для примера
        print(user)


asyncio.get_event_loop().run_until_complete(main())
