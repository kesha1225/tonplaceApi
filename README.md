# tonplaceApi

> [ton.place/tonplaceApi](https://ton.place/group7123)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Gram_cryptocurrency_logo.svg/150px-Gram_cryptocurrency_logo.svg.png)

Обертка для [ton.place](https://ton.place/kesha1225)


### Токен

Для работы вам понадобится токен, который можно получить вытащив с самого сайта из cookies или 
использовав [`token_helper`](./examples/get_token_example.py):
```python3
import asyncio

from tonplace import get_token


async def main():
    token = await get_token("79123456789")  # Ваш номер от аккаунта в телеграме
    print(token)  # bxnjkfdh42fpFlX86CJetlbwPJfbTfcz11Y1y6Obqvf5mm86WFRl3D69


asyncio.get_event_loop().run_until_complete(main())
```


## Примеры

### Парсинг новых пользователей

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