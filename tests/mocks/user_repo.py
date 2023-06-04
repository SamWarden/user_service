from typing import Dict

from src.application.user.exceptions import UserIdNotExist
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username


class UserRepoMock:
    def __init__(self):
        self.users: Dict[UserId, entities.User] = {}

    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        if user_id not in self.users:
            raise UserIdNotExist(user_id.to_uuid())
        return self.users[user_id]

    async def add_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def update_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def check_user_exists(self, user_id: UserId) -> bool:
        return user_id in self.users

    async def check_username_exists(self, username: Username) -> bool:
        usernames = {user.username for user in self.users.values()}
        return username in usernames
