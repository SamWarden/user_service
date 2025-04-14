import aio_pika
from di import Container, bind_by_type
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from user_service.application.common.interfaces.uow import UnitOfWork
from user_service.application.user.interfaces.persistence import UserReader, UserRepo
from user_service.infrastructure.db.main import build_sa_engine, build_sa_session, build_sa_session_factory
from user_service.infrastructure.db.repositories.user import UserReaderImpl, UserRepoImpl
from user_service.infrastructure.di import DiScope
from user_service.infrastructure.event_bus.event_bus import EventBusImpl
from user_service.infrastructure.mediator import get_mediator
from user_service.infrastructure.message_broker.interface import MessageBroker
from user_service.infrastructure.message_broker.main import (
    build_rq_channel,
    build_rq_channel_pool,
    build_rq_connection_pool,
    build_rq_transaction,
)
from user_service.infrastructure.message_broker.message_broker import MessageBrokerImpl
from user_service.infrastructure.uow import build_uow


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DiScope.APP, DiScope.REQUEST]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: di_builder, scope=DiScope.APP), DiBuilder))
    di_builder.bind(bind_by_type(Dependent(build_uow, scope=DiScope.REQUEST), UnitOfWork))
    setup_mediator_factory(di_builder, get_mediator, DiScope.REQUEST)
    setup_db_factories(di_builder)
    setup_event_bus_factories(di_builder)


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator))


def setup_db_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(build_sa_engine, scope=DiScope.APP), AsyncEngine))
    di_builder.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope=DiScope.APP),
            async_sessionmaker[AsyncSession],
        ),
    )
    di_builder.bind(bind_by_type(Dependent(build_sa_session, scope=DiScope.REQUEST), AsyncSession))
    di_builder.bind(bind_by_type(Dependent(UserRepoImpl, scope=DiScope.REQUEST), UserRepo, covariant=True))
    di_builder.bind(bind_by_type(Dependent(UserReaderImpl, scope=DiScope.REQUEST), UserReader, covariant=True))


def setup_event_bus_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(
            Dependent(build_rq_connection_pool, scope=DiScope.APP),
            aio_pika.pool.Pool[aio_pika.abc.AbstractConnection],
        ),
    )
    di_builder.bind(
        bind_by_type(
            Dependent(build_rq_channel_pool, scope=DiScope.APP),
            aio_pika.pool.Pool[aio_pika.abc.AbstractChannel],
        ),
    )
    di_builder.bind(
        bind_by_type(
            Dependent(build_rq_channel, scope=DiScope.REQUEST),
            aio_pika.abc.AbstractChannel,
        ),
    )
    di_builder.bind(
        bind_by_type(
            Dependent(build_rq_transaction, scope=DiScope.REQUEST),
            aio_pika.abc.AbstractTransaction,
        ),
    )
    di_builder.bind(bind_by_type(Dependent(MessageBrokerImpl, scope=DiScope.REQUEST), MessageBroker))
    di_builder.bind(bind_by_type(Dependent(EventBusImpl, scope=DiScope.REQUEST), EventBusImpl))
