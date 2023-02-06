from typing import TypedDict


class UpdateUserData(TypedDict, total=False):
    username: str
    first_name: str
    last_name: str | None
