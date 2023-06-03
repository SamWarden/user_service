from src.application.common.exceptions import MappingError
from src.domain.user.events import FullNameUpdated, UserCreated, UserDeleted, UsernameUpdated
from src.infrastructure.event_bus import events as integration_events

DomainEvents = UserCreated | UsernameUpdated | FullNameUpdated | UserDeleted


def convert_user_created_to_integration(
    event: UserCreated,
) -> integration_events.UserCreated:
    return integration_events.UserCreated(
        user_id=event.user_id,
        username=event.username,
        first_name=event.first_name,
        last_name=event.last_name,
    )


def convert_username_updated_to_integration(
    event: UsernameUpdated,
) -> integration_events.UsernameUpdated:
    return integration_events.UsernameUpdated(
        user_id=event.user_id,
        username=event.username,
    )


def convert_full_name_updated_to_integration(
    event: FullNameUpdated,
) -> integration_events.FullNameUpdated:
    return integration_events.FullNameUpdated(
        user_id=event.user_id,
        first_name=event.first_name,
        last_name=event.last_name,
        middle_name=event.middle_name,
    )


def convert_user_deleted_to_integration(
    event: UserDeleted,
) -> integration_events.UserDeleted:
    return integration_events.UserDeleted(
        user_id=event.user_id,
    )


def convert_domain_event_to_integration(
    event: DomainEvents,
) -> integration_events.IntegrationEvent:
    match event:
        case UserCreated():
            return convert_user_created_to_integration(event)
        case UsernameUpdated():
            return convert_username_updated_to_integration(event)
        case FullNameUpdated():
            return convert_full_name_updated_to_integration(event)
        case UserDeleted():
            return convert_user_deleted_to_integration(event)
        case _:
            raise MappingError(f"Event {event} cannot be mapped to integration event")
