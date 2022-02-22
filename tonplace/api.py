import json
from json import JSONDecodeError
from typing import Optional

import aiohttp


class API:
    def __init__(self, token: str, return_error: bool = False):
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
        self.return_error = return_error

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ):
        resp = await self.session.request(
            method,
            self.base_path + path,
            data=data,
            json=json_data,
            headers=self.headers,
        )
        if resp.status >= 500:
            raise ValueError("Site is down")
        try:
            json_response = json.loads(await resp.text())
        except JSONDecodeError:
            if self.return_error:
                return await resp.text()
            raise ValueError(
                f"Ошибка декодирования json ответа, чтобы получать ошибки - return_error=True"
            )
        if isinstance(json_response, str):
            return json_response
        if json_response.get("code") == "fatal":
            if self.return_error:
                return await resp.text()
            raise ValueError(
                f"Ошибка запроса - {json_response.get('message')}, чтобы получать ошибки - return_error=True"
            )
        return json_response

    async def get_user(self, user_id: int):
        """
        Информация о юзере в том числе посты
        :param user_id:
        :return:
        """
        user = await self.request("POST", path=f"profile/{user_id}")
        return user

    async def get_group(self, group_id: int):
        """
        Информация о группе в том числе посты
        :param group_id:
        :return:
        """
        user = await self.request("POST", path=f"/group/{group_id}")
        return user

    async def search(
        self,
        tab: str,
        sort: str = "popular",
        query: str = "",
        city: int = 0,
        start_from: int = 0,
    ):
        """
        Поиск (возвращает 30 элементов)

        :param tab: peoples|groups
        :param sort: popular|new|online
        :param query: поисковой запрос
        :param start_from: offset
        :param city: по дефолту пока всегда 0
        :return:
        """
        result = await self.request(
            "POST",
            path=f"search",
            json_data={
                "query": query,
                "startFrom": start_from,
                "tab": tab,
                "sort": sort,
                "city": city,
            },
        )
        return result

    async def follow(self, user_id: int):
        result = await self.request(
            "POST",
            path=f"follow/{user_id}/add",
        )
        return result

    async def unfollow(self, user_id: int):
        result = await self.request(
            "POST",
            path=f"follow/{user_id}/del",
        )
        return result

    async def like(self, post_id: int):
        result = await self.request(
            "POST",
            path=f"likes/{post_id}/post/add",
        )
        return result

    async def write_comment(
        self,
        post_id: int,
        text: str,
        attachments: Optional[list] = None,
        reply: Optional[int] = 0,
        group_id: Optional[int] = 0,
    ):
        if attachments is None:
            attachments = []
        result = await self.request(
            "POST",
            path=f"posts/new",
            json_data={
                "parentId": post_id,
                "replyTo": reply,
                "text": text,
                "attachments": attachments,
                "groupId": group_id,
            },
        )
        return result

    async def read_post(self, post_id: int):
        """
        Засчитывает просмотр посту
        :param post_id:
        :return:
        """
        result = await self.read_posts([post_id])
        return result

    async def read_posts(self, post_ids: list[int]):
        """
        Засчитывает просмотр постам
        :param post_ids:
        :return:
        """
        result = await self.request(
            "POST",
            path=f"posts/read",
            json_data={
                "posts": post_ids,
            },
        )
        return result

    async def get_post(self, post_id: int):
        result = await self.request(
            "GET",
            path=f"posts/{post_id}",
        )
        return result

    async def get_feed(self, section: str, start_from: int = 0, suggestions: Optional[bool] = None):
        """
        Получить ленту

        :param section: - following|suggestions|liked (подписки, рекомендации, понравилось)
        :param start_from: - offset
        :param suggestions:
        :return:
        """
        if suggestions is None and section != "suggestions":
            suggestions = False

        result = await self.request(
            "POST",
            path=f"feed",
            json_data={
                "section": section,
                "startFrom": start_from,
                "suggestions": suggestions
            }
        )
        return result

    async def get_dialogs(self):
        pass

    async def close(self):
        await self.session.close()
