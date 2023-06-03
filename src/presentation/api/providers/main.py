from di import ScopeState
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import FastAPI

from src.application.common.interfaces.mapper import Mapper
from src.presentation.api.presenter import Presenter, build_presenter

from .di import StateProvider, get_di_builder, get_di_state
from .mediator import MediatorProvider
from .stub import Stub


def setup_providers(
    app: FastAPI,
    mediator: Mediator,
    mapper: Mapper,
    di_builder: DiBuilder,
    di_state: ScopeState | None = None,
) -> None:
    mediator_provider = MediatorProvider(mediator)

    app.dependency_overrides[Stub(Mediator)] = mediator_provider.build
    app.dependency_overrides[Stub(CommandMediator)] = mediator_provider.build
    app.dependency_overrides[Stub(QueryMediator)] = mediator_provider.build
    app.dependency_overrides[Stub(EventMediator)] = mediator_provider.build

    app.dependency_overrides[Stub(Mapper)] = lambda: mapper

    state_provider = StateProvider(di_state)

    app.dependency_overrides[get_di_builder] = lambda: di_builder
    app.dependency_overrides[get_di_state] = state_provider.build

    presenter = build_presenter()

    app.dependency_overrides[Stub(Presenter)] = lambda: presenter
