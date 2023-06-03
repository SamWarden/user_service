import logging

from didiator import CommandDispatcherImpl, EventObserverImpl, Mediator, MediatorImpl, QueryDispatcherImpl
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiMiddleware, DiScopes
from didiator.middlewares.logging import LoggingMiddleware

from src.application.user.commands import (
    CreateUser,
    CreateUserHandler,
    DeleteUser,
    DeleteUserHandler,
    SetUserFullName,
    SetUserFullNameHandler,
    SetUserUsername,
    SetUserUsernameHandler,
)
from src.application.user.queries.get_user_by_id import GetUserById, GetUserByIdHandler
from src.application.user.queries.get_user_by_username import GetUserByUsername, GetUserByUsernameHandler
from src.application.user.queries.get_users import GetUsers, GetUsersHandler
from src.domain.common.events import Event
from src.infrastructure.di import DiScope
from src.infrastructure.event_bus.event_handler import EventHandlerPublisher
from src.infrastructure.log.event_handler import EventLogger


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(DiScope.REQUEST)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(CreateUser, CreateUserHandler)
    mediator.register_command_handler(SetUserUsername, SetUserUsernameHandler)
    mediator.register_command_handler(SetUserFullName, SetUserFullNameHandler)
    mediator.register_command_handler(DeleteUser, DeleteUserHandler)
    mediator.register_query_handler(GetUserById, GetUserByIdHandler)
    mediator.register_query_handler(GetUserByUsername, GetUserByUsernameHandler)
    mediator.register_query_handler(GetUsers, GetUsersHandler)
    mediator.register_event_handler(Event, EventLogger)
    mediator.register_event_handler(Event, EventHandlerPublisher)
