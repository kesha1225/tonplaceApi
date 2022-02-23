"""
парсинг популярных групп и лайкание рандомных комментариев
"""

import asyncio
import random

from tonplace import get_token, API


async def main():
    token = await get_token("+7912345789", save_session=True)
    api = API(token)

    popular_groups = await api.search(tab="groups", sort="popular")

    target_comments = []
    for group_id in list(popular_groups["groups"].keys())[
        :2
    ]:  # берем из двух популярных групп
        group_data = await api.get_group(group_id)
        posts = group_data["posts"]

        for post in posts[:2]:  # берем из двух последних постов
            post_data = await api.get_post(post["id"])
            comments = post_data["comments"]
            if not comments:
                continue

            print(
                f"Лайкнули комменты тут - https://ton.place/group{group_id}?w=post{post['id']}"
            )
            for _ in range(2):  # выбираем 2 рандомных коммента
                if not comments:  # комментов было меньше чем 2
                    break
                target_comments.append(comments.pop(random.randrange(len(comments))))

    for comment in target_comments:
        await api.like(comment["id"])


asyncio.get_event_loop().run_until_complete(main())
