from typing import Optional

from ...channel import models
from ...permission.auth_filters import is_app, is_staff_user
from ..core.context import get_database_connection_name
from ..core.utils import from_global_id_or_error
from ..core.validators import validate_one_of_args_is_in_query
from .types import Channel


def resolve_channel(info, id: Optional[str], slug: Optional[str]):
    validate_one_of_args_is_in_query("id", id, "slug", slug)
    if id:
        _, db_id = from_global_id_or_error(id, Channel)
        channel = (
            models.Channel.objects.using(get_database_connection_name(info.context))
            .filter(id=db_id)
            .first()
        )
    else:
        channel = (
            models.Channel.objects.using(get_database_connection_name(info.context))
            .filter(slug=slug)
            .first()
        )

    if channel and channel.is_active:
        return channel
    if is_staff_user(info.context) or is_app(info.context):
        return channel

    return None


# def resolve_channels(info):
#     return models.Channel.objects.using(
#         get_database_connection_name(info.context)
#     ).all()

def resolve_channels(info):
    """
    Resolves the list of channels accessible to the user.

    Returns only channels the user has permissions for.
    """
    from ...graphql.account.dataloaders import AccessibleChannelsByUserIdLoader

    # Retrieve the requestor (user or app) from the context
    requestor = info.context.user

    # Check if the requestor is a staff user or an app
    if is_app(info.context):
        # For staff or apps, return all channels
        return models.Channel.objects.using(
            get_database_connection_name(info.context)
        ).all()

    # For regular users, retrieve accessible channels
    if requestor and hasattr(requestor, "id"):
        accessible_channels_promise = AccessibleChannelsByUserIdLoader(
            info.context
        ).load(requestor.id)

        def filter_accessible_channels(accessible_channels):
            accessible_channel_ids = [channel.id for channel in accessible_channels]
            return models.Channel.objects.using(
                get_database_connection_name(info.context)
            ).filter(id__in=accessible_channel_ids)

        return accessible_channels_promise.then(filter_accessible_channels)

    # If no valid requestor is found, return an empty queryset
    return models.Channel.objects.none()