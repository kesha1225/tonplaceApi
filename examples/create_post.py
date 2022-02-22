import asyncio

from tonplace import get_token, API, Attachments


async def main():
    token = await get_token("+79123456789", save_session=True)
    api = API(token)

    with open("./assets/killer.jpg", "rb") as f:
        data = f.read()

    photo_data = await api.upload_photo(data)

    photo_id = photo_data["photo_id"]

    my_groups = await api.get_owned_groups()
    target_group_id = list(my_groups["groups"].keys())[0]
    # первая группа которой мы владеем, иначе айди можно просто взять из ссылки https://ton.place/group123
    attachments = Attachments()
    attachments.add_photo(photo_id)

    # айди группы вовзращается без минуса а для поста нужно указывать с минусом
    res = await api.create_post(owner_id=-int(target_group_id), attachments=attachments)

    print(f"Результат - https://ton.place/group{target_group_id}?w=post{res['post']['id']}")

    await api.close()


asyncio.get_event_loop().run_until_complete(main())
