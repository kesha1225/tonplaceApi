import io
import json
from json import JSONDecodeError
from typing import Optional, Union

import aiohttp


class API:
    def __init__(self, token: str, return_error: bool = False):
        self.session = aiohttp.ClientSession()
        self.token = token
        self.base_path = "https://api.ton.place/"
        self.upload_path = "https://upload.ton.place/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        self.return_error = return_error

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[Union[str, io.BytesIO]] = None,
        json_data: Optional[dict] = None,
        extra_headers: Optional[dict] = None,
    ):
        current_headers = self.headers
        if extra_headers:
            current_headers.update(extra_headers)
        print(current_headers)
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

        :param tab: explore|peoples|groups
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
        text: str = "",
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

    async def get_feed(
        self, section: str, start_from: int = 0, suggestions: Optional[bool] = None
    ):
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
                "suggestions": suggestions,
            },
        )
        return result

    async def get_dialogs(self):
        result = await self.request(
            "GET",
            path=f"im",
        )
        return result

    async def get_notify(self):
        result = await self.request(
            "GET",
            path=f"notify",
        )
        return result

    async def get_owned_groups(self):
        result = await self.request(
            "GET",
            path=f"groups",
        )
        return result

    async def get_balance(self):
        result = await self.request(
            "GET",
            path=f"balance",
        )
        return result

    async def send_ton(self, address: str, amount: float):
        result = await self.request(
            "POST",
            path=f"/balance/withdraw",
            json_data={
                "address": address,
                "amount": amount,
            },
        )
        return result

    async def create_post(
        self,
        owner_id: int,
        text: str = "",
        parent_id: int = 0,
        timer: int = 0,
        attachments: Optional[list] = None,
    ):
        """
        Создать пост
        :param owner_id: айди страницы или группы
        :param text:
        :param parent_id:
        :param timer:
        :param attachments:
        :return:
        """
        if attachments is None:
            attachments = []
        result = await self.request(
            "POST",
            path=f"/posts/new",
            json_data={
                "attachments": attachments,
                "ownerId": owner_id,
                "parentId": parent_id,
                "text": text,
                "timer": timer,
            },
        )
        return result

    async def close(self):
        await self.session.close()
