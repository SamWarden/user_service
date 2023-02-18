from dataclasses import dataclass

import pytest
from adaptix import dumper, loader, Omitted, Retort
from adaptix.load_error import TypeLoadError

from src.infrastructure.mapper.converter import Converter


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


@dataclass
class OrderOwner(User):
    orders: list[Order]


@dataclass
class OrderOwnerDTO(UserDTO):
    orders: list[OrderDTO]


DTOs = OrderDTO | UserDTO | OrderOwnerDTO


@dataclass
class UserModel:
    user_id: int
    username: str


# Converters


def convert_user_entity_to_dto(user: User) -> UserDTO:
    return UserDTO(
        user_id=str(user.id),
        username=user.username,
    )


def convert_order_entity_to_dto(order: Order) -> OrderDTO:
    return OrderDTO(
        order_id=order.id,
        owner_id=order.owner_id,
    )


def convert_order_owner_entity_to_dto(order_owner: OrderOwner) -> OrderOwnerDTO:
    return OrderOwnerDTO(
        user_id=str(order_owner.id),
        username=order_owner.username,
        orders=[
            OrderDTO(order_id=order.id, owner_id=order.owner_id)
            for order in order_owner.orders
        ],
    )


def convert_user_model_to_dto(user: UserModel) -> UserDTO:
    return UserDTO(
        user_id=str(user.user_id),
        username=user.username,
    )


# Tests


def test_convert_entity_to_dto():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
    ))

    assert retort.load(User(1, "Jon"), UserDTO) == UserDTO("1", "Jon")


def test_raise_error_on_wrong_entity_conversion():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
    ))

    with pytest.raises(TypeLoadError):
        retort.load(Order(1, 100), UserDTO)


def test_convert_entity_to_unknown_dto():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
        Converter(Order, OrderDTO, convert_order_entity_to_dto),
    ))

    assert retort.load(User(1, "Jon"), UserDTO) == UserDTO("1", "Jon")
    assert retort.load(Order(1, 100), OrderDTO) == OrderDTO(1, 100)
    assert retort.load(User(1, "Jon"), DTOs) == UserDTO("1", "Jon")
    assert retort.load(Order(1, 100), DTOs) == OrderDTO(1, 100)


def test_convert_sequence_entities_to_list_dtos():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
        Converter(Order, OrderDTO, convert_order_entity_to_dto),
    ))

    assert retort.load([User(1, "Jon"), Order(1, 100)], list[DTOs]) == [UserDTO("1", "Jon"), OrderDTO(1, 100)]
    assert retort.load((User(1, "Jon"), Order(1, 100)), list[DTOs]) == [UserDTO("1", "Jon"), OrderDTO(1, 100)]


@pytest.mark.skip("Convert to tuple of dataclasses not working now")
def test_convert_sequence_entities_to_tuple_dtos():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
        Converter(Order, OrderDTO, convert_order_entity_to_dto),
    ))

    assert retort.load((User(1, "Jon"), Order(1, 100)), tuple[UserDTO, OrderDTO]) == (UserDTO("1", "Jon"), OrderDTO(1, 100))
    assert retort.load((User(1, "Jon"), Order(1, 100)), tuple[DTOs, DTOs]) == (UserDTO("1", "Jon"), OrderDTO(1, 100))
    assert retort.load((User(1, "Jon"), Order(1, 100)), tuple[DTOs, ...]) == (UserDTO("1", "Jon"), OrderDTO(1, 100))


def test_convert_order_owner_entity_to_dto():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
        Converter(Order, OrderDTO, convert_order_entity_to_dto),
        Converter(OrderOwner, OrderOwnerDTO, convert_order_owner_entity_to_dto),
    ))

    assert retort.load(
        OrderOwner(1, "Jon", [Order(1, 100), Order(2, 200)]),
        OrderOwnerDTO,
    ) == OrderOwnerDTO("1", "Jon", [OrderDTO(1, 100), OrderDTO(2, 200)])


def test_convert_model_to_user_dto():
    retort = Retort(recipe=(
        Converter(User, UserDTO, convert_user_entity_to_dto),
        Converter(UserModel, UserDTO, convert_user_model_to_dto),
    ))

    assert retort.load(User(1, "Jon"), UserDTO) == UserDTO("1", "Jon")
    assert retort.load(UserModel(1, "Jon"), UserDTO) == UserDTO("1", "Jon")
