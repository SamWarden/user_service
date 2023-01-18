from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.container import bind_by_type, Container
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.utils.di_builder import DiBuilder
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.application.commands.common.interfaces.persistence import UserRepo
from src.application.common.base.interfaces.mapper import Mapper
from src.application.common.base.interfaces.uow import UnitOfWork
from src.application.queries.common.interfaces.persistence import UserReader
from src.infrastructure.constants import APP_SCOPE, REQUEST_SCOPE
from src.infrastructure.db.main import build_sa_engine, build_sa_session, build_sa_session_factory
from src.infrastructure.db.repositories.user import UserReaderImpl, UserRepoImpl
from src.infrastructure.db.uow import SQLAlchemyUoW
from src.infrastructure.factories.mediator import build_mediator
from src.infrastructure.mapper.main import build_mapper, MapperImpl


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator))


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = (APP_SCOPE, REQUEST_SCOPE)
    di_builder = DiBuilder(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: di_builder, scope=APP_SCOPE), DiBuilder))
    di_builder.bind(bind_by_type(Dependent(build_mapper, scope=APP_SCOPE), Mapper))
    setup_mediator_factory(di_builder, build_mediator, APP_SCOPE)

    di_builder.bind(bind_by_type(Dependent(build_sa_engine, scope=APP_SCOPE), AsyncEngine))
    di_builder.bind(bind_by_type(Dependent(build_sa_session_factory, scope=APP_SCOPE), sessionmaker))
    di_builder.bind(bind_by_type(Dependent(build_sa_session, scope=REQUEST_SCOPE), AsyncSession))
    di_builder.bind(bind_by_type(Dependent(SQLAlchemyUoW, scope=REQUEST_SCOPE), UnitOfWork))
    di_builder.bind(bind_by_type(Dependent(UserRepoImpl, scope=REQUEST_SCOPE), UserRepo, covariant=True))
    di_builder.bind(bind_by_type(Dependent(UserReaderImpl, scope=REQUEST_SCOPE), UserReader, covariant=True))
