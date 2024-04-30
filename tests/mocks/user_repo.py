from src.application.user.exceptions import UserIdNotExistError
from src.application.user.interfaces import UserRepo
from src.domain.user import entities
from src.domain.user.value_objects import UserId, Username


class UserRepoMock(UserRepo):
    def __init__(self) -> None:
        self.users: dict[UserId, entities.User] = {}

    async def acquire_user_by_id(self, user_id: UserId) -> entities.User:
        if user_id not in self.users:
            raise UserIdNotExistError(user_id.to_raw())
        return self.users[user_id]

    async def add_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def update_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def get_existing_usernames(self) -> set[Username]:
        usernames = {user.username for user in self.users.values()}
        return usernames
