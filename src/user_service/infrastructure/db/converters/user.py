from typing import Any, cast

from user_service.application.user import dto


def convert_db_row_to_user_dto(user_row: Any) -> dto.User:
    return dto.User(
        id=user_row.id,
        username=cast(str, user_row.username),
        first_name=user_row.first_name,
        last_name=user_row.last_name,
        middle_name=user_row.middle_name,
        deleted_at=user_row.deleted_at,
    )
