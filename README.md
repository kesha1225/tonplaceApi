# tonplaceApi

> [ton.place/tonplaceApi](https://ton.place/group7123)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Gram_cryptocurrency_logo.svg/150px-Gram_cryptocurrency_logo.svg.png)

Обертка для [ton.place](https://ton.place/kesha1225)


### Установка

```
pip install https://github.com/kesha1225/tonplaceApi/archive/master.zip
```


### Токен

Для работы вам понадобится токен, который можно получить вытащив с самого сайта из cookies или 
использовав [`token_helper`](./examples/get_token_example.py):
```python3
import asyncio

from tonplace import get_token


async def main():
    token = await get_token("79123456789", save_session=True)  # Ваш номер от аккаунта в телеграме
    # save_session сохраняет токены номеров в файлы и при следующем вызове get_token достает их
    print(token)  # bxnjkfdh42fpFlX86CJetlbwPJfbTfcz11Y1y6Obqvf5mm86WFRl3D69


asyncio.get_event_loop().run_until_complete(main())
```


## [Примеры](examples/)

### Любой запрос к ton.place
```python3
custom_data = await api.request("POST", path=f"test/test", json_data={"test": 123})
```

### Парсинг новых пользователей
```python3
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
```


### Парсинг популярных групп, лайк, коммент, фолоу
```python3
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
        print(f"Зафоловились на автора поста - https://ton.place/id{post_author}")


asyncio.get_event_loop().run_until_complete(main())
```
