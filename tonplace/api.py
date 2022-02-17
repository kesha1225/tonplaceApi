import json
from typing import Optional

import aiohttp


class API:
    def __init__(self, token: str):
        self.session = aiohttp.ClientSession()
        self.token = token
        self.base_path = "https://api.ton.place/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru",
            "Content-Type": "application/json",
            "Authorization": token,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
        }

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ):
        resp = await self.session.request(
            method, self.base_path + path, data=data, json=json_data
        )
        json_response = json.loads(await resp.text())
        if json_response.get("code") == "fatal":
            raise ValueError(f"Ошибка запроса - {json_response.get('message')}")
        return json_response

    async def get_user(self, user_id: int):
        user = await self.request("POST", path=f"profile/{user_id}")
        return user

    async def search(self, tab: str, sort: str = "popular", city: int = 0, start_from: int = 0):
        """
        Поиск (возвращает 30 элементов)

        :param tab: peoples|groups
        :param sort: popular|new|online
        :param start_from: offset
        :param city: по дефолту пока всегда 0
        :return:
        """
        result = await self.request(
            "POST",
            path=f"search",
            json_data={
                "query": "",
                "startFrom": start_from,
                "tab": tab,
                "sort": sort,
                "city": city,
            },
        )
        return result

    async def close(self):
        await self.session.close()
