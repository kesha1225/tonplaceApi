"""
Кастомный реквест на метод который не прописан
"""
import asyncio

from tonplace import get_token, API


async def main():
    token = await get_token("+79123456789", save_session=True)
    api = API(token)

    # Любой запрос к ton.place api которого нет в методах
    custom_data = await api.request("POST", path=f"test/test", json_data={"test": 123})
    return custom_data


asyncio.get_event_loop().run_until_complete(main())
