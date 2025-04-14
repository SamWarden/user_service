import pytest
from user_service.domain.user.interfaces.repo import UserRepo
from user_service.domain.user.service import UserService

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock
from tests.mocks.user_reader import UserReaderMock


@pytest.fixture()
def user_repo() -> UserRepoMock:
    return UserRepoMock()


@pytest.fixture()
def user_reader() -> UserReaderMock:
    return UserReaderMock()


@pytest.fixture()
def event_mediator() -> EventMediatorMock:
    return EventMediatorMock()


@pytest.fixture()
def uow() -> UnitOfWorkMock:
    return UnitOfWorkMock()


@pytest.fixture()
def user_service(user_repo: UserRepo) -> UserService:
    return UserService(user_repo)
