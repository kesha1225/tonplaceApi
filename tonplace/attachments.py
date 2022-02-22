class Attachments:
    def __init__(self):
        self._attachments: list[dict[str, str]] = []

    def add_photo(self, photo_id: int):
        self._attachments.append({"type": "photo", "photo": {"photoId": photo_id}})
        return self

    def get_attachments(self):
        return self._attachments
