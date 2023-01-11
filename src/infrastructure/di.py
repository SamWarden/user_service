from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.container import bind_by_type, Container
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.utils.di_builder import DiBuilder

from src.application.base.interfaces.mapper import Mapper
from src.infrastructure.constants import APP_SCOPE, REQUEST_SCOPE
from src.infrastructure.factories.mediator import build_mediator
from src.infrastructure.mapper.main import build_mapper


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator))


def setup_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = (APP_SCOPE, REQUEST_SCOPE)
    di_builder = DiBuilder(di_container, di_executor, di_scopes=di_scopes)

    di_builder.bind(bind_by_type(Dependent(lambda *args: di_builder, scope=APP_SCOPE), DiBuilder))
    di_builder.bind(bind_by_type(Dependent(build_mapper, scope=APP_SCOPE), Mapper))
    setup_mediator_factory(di_builder, build_mediator, APP_SCOPE)

    # di_builder.bind(bind_by_type(Dependent(build_config, scope=APP_SCOPE), Config))
    # di_builder.bind(bind_by_type(Dependent(build_sa_engine, scope=APP_SCOPE), AsyncEngine))
    # di_builder.bind(bind_by_type(Dependent(build_sa_pool, scope=APP_SCOPE), sessionmaker))
    # di_builder.bind(bind_by_type(Dependent(build_sa_session, scope=REQUEST_SCOPE), AsyncSession))
    # di_builder.bind(bind_by_type(Dependent(build_repo, scope=REQUEST_SCOPE), UserRepo))
    return di_builder
