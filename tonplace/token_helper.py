import json
import time
from typing import Optional

import aiohttp

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "referrer": "https://ton.place/",
    "origin": "https://ton.place/",
}


def write_session(phone: str, token: str):
    with open(f"session_{phone}", "w") as session:
        session.write(token)


def read_session(phone: str) -> Optional[str]:
    try:
        with open(f"session_{phone}") as session:
            return session.read()
    except FileNotFoundError:
        return None


async def get_token(phone: str, save_session: bool = False) -> str:
    """
    :param phone:
    :param save_session: save token in file
    :return:
    """
    session = aiohttp.ClientSession()
    token = read_session(phone)
    if token is not None:
        return token
    await session.post(
        "https://oauth.telegram.org/auth?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )

    await session.post(
        "https://oauth.telegram.org/auth/request?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
        data=f"phone={phone}",
    )

    input("Подтвердите аутентификацию в телеграме и нажмите Enter:")

    await session.post(
        "https://oauth.telegram.org/auth/login?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )
    await session.post(
        "https://oauth.telegram.org/auth/login?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )
    await session.post(
        "https://oauth.telegram.org/auth/login?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )

    await session.get(
        "https://oauth.telegram.org/auth?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )

    await session.get(
        "https://oauth.telegram.org/auth/push?bot_id=2141264283&origin=https://ton.place",
        headers=DEFAULT_HEADERS,
    )

    resp = await session.post(
        "https://oauth.telegram.org/auth/get",
        headers=DEFAULT_HEADERS,
        data="bot_id=2141264283",
    )

    user = await resp.json()
    if user.get("user") is None:
        raise ValueError("Не авторизовано. Попробуйте снова.")
    user = user["user"]
    user["id"] = str(user["id"])

    await session.options(
        "https://api.ton.place/auth/telegram",
        headers=DEFAULT_HEADERS,
    )

    json_data = {
        "device": f"chrome_{int(time.time())}",
        "params": {
            "id": user["id"],
            "first_name": user["first_name"],
            "username": user["username"],
            "auth_date": str(user["auth_date"]),
            "hash": user["hash"],
        },
    }
    if "photo_url" in user:
        json_data["params"]["photo_url"] = user["photo_url"]

    resp = await session.post(
        "https://api.ton.place/auth/telegram",
        headers=DEFAULT_HEADERS,
        json=json_data,
    )
    response_json = json.loads(await resp.text())
    if response_json.get("code") == "fatal":
        raise ValueError(f"Неверный хеш, попробуйте еще раз. Ошибка - {response_json}")

    token = response_json["access_token"]

    await session.close()
    if save_session:
        write_session(phone, token)
    return token
