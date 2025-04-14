from user_service.domain.user import entities
from user_service.domain.user.interfaces.repo import UserRepo
from user_service.domain.user.value_objects import UserId, Username


class UserRepoMock(UserRepo):
    def __init__(self) -> None:
        self.users: dict[UserId, entities.User] = {}

    async def acquire_user_by_id(self, user_id: UserId) -> entities.User | None:
        return self.users.get(user_id)

    async def add_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def check_username_exists(self, username: Username) -> bool:
        username_exists = next((True for user in self.users.values() if user.username == username), False)
        return username_exists
