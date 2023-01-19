import logging
from collections.abc import Callable

import structlog
from di.container import ContainerState
from didiator import CommandDispatcherImpl, EventObserverImpl, Mediator, MediatorImpl, QueryDispatcherImpl
from didiator.middlewares.di import DiMiddleware
from didiator.middlewares.logging import LoggingMiddleware
from didiator.utils.di_builder import DiBuilder

from src.application.user.commands import CreateUser, CreateUserHandler
from src.application.user.commands import DeleteUser, DeleteUserHandler
from src.application.user.commands import UpdateUser, UpdateUserHandler
from src.application.user.queries.get_user_by_id import GetUserById, GetUserByIdHandler
from src.application.user.queries.get_user_by_username import GetUserByUsername, GetUserByUsernameHandler
from src.application.user.queries.get_users import GetUsers, GetUsersHandler
from src.infrastructure.constants import REQUEST_SCOPE


def build_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware(structlog.get_logger("mediator"), level=logging.DEBUG),
        DiMiddleware(di_builder, cls_scope=REQUEST_SCOPE),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    mediator.register_command_handler(CreateUser, CreateUserHandler)
    mediator.register_command_handler(UpdateUser, UpdateUserHandler)
    mediator.register_command_handler(DeleteUser, DeleteUserHandler)
    mediator.register_query_handler(GetUserById, GetUserByIdHandler)
    mediator.register_query_handler(GetUserByUsername, GetUserByUsernameHandler)
    mediator.register_query_handler(GetUsers, GetUsersHandler)
    # mediator.register_event_handler(UserCreated, UserCreatedHandler)

    return mediator


def create_mediator_builder(mediator: Mediator) -> Callable[[ContainerState], Mediator]:
    def _build_mediator(di_state: ContainerState) -> Mediator:
        return mediator.bind(di_state=di_state)
    return _build_mediator
