from dataclasses import dataclass

import pytest
from dataclass_factory import Retort, loader
from dataclass_factory.load_error import ValueLoadError


@dataclass
class User:
    id: int
    username: str


@dataclass
class Order:
    id: int
    owner_id: int


@dataclass
class DTO:
    pass


@dataclass
class UserDTO(DTO):
    user_id: str
    username: str


@dataclass
class OrderDTO(DTO):
    order_id: int
    owner_id: int


DTOs = OrderDTO | UserDTO


def convert_user_entity_to_dto(user: User) -> UserDTO:
    if not isinstance(user, User):
        raise ValueLoadError(f"Wrong type, user is not User: {type(user)}")

    return UserDTO(
        user_id=str(user.id),
        username=user.username,
    )


def convert_order_entity_to_dto(order: Order) -> OrderDTO:
    if not isinstance(order, Order):
        raise ValueLoadError(f"Wrong type, order is not Order: {type(order)}")

    return OrderDTO(
        order_id=order.id,
        owner_id=order.owner_id,
    )


def test_convert_entity_to_dto():
    retort = Retort(recipe=(
        loader(UserDTO, convert_user_entity_to_dto),
    ))

    assert retort.load(User(1, "Jon"), UserDTO) == UserDTO("1", "Jon")


def test_raise_error_on_wrong_entity_conversion():
    retort = Retort(recipe=(
        loader(UserDTO, convert_user_entity_to_dto),
    ))

    with pytest.raises(ValueLoadError):
        retort.load(Order(1, 100), UserDTO)


def test_convert_entity_to_unknown_dto():
    retort = Retort(recipe=(
        loader(UserDTO, convert_user_entity_to_dto),
        loader(OrderDTO, convert_order_entity_to_dto),
    ))

    assert retort.load(User(1, "Jon"), UserDTO) == UserDTO("1", "Jon")
    assert retort.load(Order(1, 100), OrderDTO) == OrderDTO(1, 100)
    assert retort.load(User(1, "Jon"), DTOs) == UserDTO("1", "Jon")
    assert retort.load(Order(1, 100), DTOs) == OrderDTO(1, 100)
