import pytest
from didiator import EventMediator

from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import UserRepo
from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


@pytest.fixture
def user_repo() -> UserRepo:
    return UserRepoMock()


@pytest.fixture
def event_mediator() -> EventMediator:
    return EventMediatorMock()


@pytest.fixture
def uow() -> UnitOfWork:
    return UnitOfWorkMock()
