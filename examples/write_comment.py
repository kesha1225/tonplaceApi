"""
Написание комментария на посты в популярных группах
"""
import asyncio

from tonplace import get_token, API


async def main():
    token = await get_token("+79123456789")
    api = API(token)

    popular_groups = await api.search(tab="groups", sort="popular")
    for group_id in popular_groups["groups"]:
        group_data = await api.get_group(group_id)
        posts = group_data["posts"]
        target_post = posts[0]

        target_id = target_post["id"]
        await api.write_comment(target_id, text="test")
        await api.like(target_id)
        print(
            f"Написали коммент и лайкнули пост - https://ton.place/group{group_id}?w=post{target_id}"
        )

        post_author = target_post["ownerId"]
        await api.follow(post_author)
        # на автора поста тоже можно зафоловиться, его айди лежит в target_post (creatorId или типа того)
        print(f"Зафоловились на группу - https://ton.place/id{post_author}")


asyncio.get_event_loop().run_until_complete(main())
