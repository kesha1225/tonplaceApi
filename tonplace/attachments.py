from typing import Optional


class Attachments:
    def __init__(self):
        self._attachments: list[dict[str, str]] = []

    def add_photo(
        self, photo_id: Optional[int] = None, photo_data: Optional[dict] = None
    ):
        """
        Можно передать айди фото напрямую или словарь формата {"photo_id":675770} который возвращает upload запрос
        :param photo_id:
        :param photo_data:
        :return:
        """
        if photo_id is None and photo_data is None:
            raise ValueError("no photo data")
        if photo_data is not None:
            photo_id = photo_data.get("photo_id")
        if photo_id is None:
            raise ValueError("wrong photo data")

        self._attachments.append({"type": "photo", "photo": {"photoId": photo_id}})
        return self

    def add_video(
        self, video_id: Optional[int] = None, video_data: Optional[dict] = None
    ):
        """
        Можно передать айди видео напрямую или словарь формата
         {'videoId': 49815, 'poster': '123.png'} который возвращает upload запрос
        :param video_id:
        :param video_data:
        :return:
        """
        if video_id is None and video_data is None:
            raise ValueError("no video data")
        if video_data is not None:
            video_id = video_data.get("videoId")
        if video_id is None:
            raise ValueError("wrong video data")

        self._attachments.append({"type": "video", "video": {"videoId": video_id}})
        return self

    def get_attachments(self):
        return self._attachments
