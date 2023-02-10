from src.domain.user.events import UserCreated, UserDeleted, UserUpdated
from src.infrastructure.event_bus import events as integration_events


def convert_user_created_to_integration(event: UserCreated) -> integration_events.UserCreated:
    return integration_events.UserCreated(
        user_id=event.user_id,
        username=event.username,
        first_name=event.first_name,
        last_name=event.last_name,
    )


def convert_user_updated_to_integration(event: UserUpdated) -> integration_events.UserUpdated:
    return integration_events.UserUpdated(
        user_id=event.user_id,
        username=event.username,
        first_name=event.first_name,
        last_name=event.last_name,
    )


def convert_user_deleted_to_integration(event: UserDeleted) -> integration_events.UserDeleted:
    return integration_events.UserDeleted(
        user_id=event.user_id,
    )
