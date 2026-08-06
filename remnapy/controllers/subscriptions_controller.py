from typing import Annotated, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    GetAllSubscriptionsResponseDto,
    GetConnectionKeysByUserIdResponseDto,
    GetRawSubscriptionByShortUuidResponseDto,
    GetSubpageConfigByShortUuidRequestBodyDto,
    GetSubpageConfigByShortUuidResponseDto,
    GetSubscriptionByShortUUIDResponseDto,
    GetSubscriptionByUserIdResponseDto,
    GetSubscriptionByUsernameResponseDto,
)
from remnapy.rapid import BaseController, get


class SubscriptionsController(BaseController):
    # Protected endpoints below
    @get("/subscriptions", response_class=GetAllSubscriptionsResponseDto)
    async def get_all_subscriptions(
        self,
        start: Annotated[
            int, Query(default=0, ge=0, description="Index to start pagination from")
        ],
        size: Annotated[
            int, Query(default=25, ge=1, description="Number of users per page")
        ],
    ) -> GetAllSubscriptionsResponseDto:
        """None"""
        ...

    @get(
        "/subscriptions/by-username/{username}",
        response_class=GetSubscriptionByUsernameResponseDto,
    )
    async def get_subscription_by_username(
        self,
        username: Annotated[str, Path(description="Username of the user")],
    ) -> GetSubscriptionByUsernameResponseDto:
        """None"""
        ...

    @get(
        "/subscriptions/by-short-uuid/{shortUuid}",
        response_class=GetSubscriptionByShortUUIDResponseDto,
    )
    async def get_subscription_by_short_uuid(
        self,
        short_uuid: Annotated[
            Union[str, UUID],
            Path(description="Short UUID of the subscription", alias="shortUuid"),
        ],
    ) -> GetSubscriptionByShortUUIDResponseDto:
        """None"""
        ...

    @get(
        "/subscriptions/by-id/{userId}", response_class=GetSubscriptionByUserIdResponseDto
    )
    async def get_subscription_by_user_id(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetSubscriptionByUserIdResponseDto:
        """Get subscription by User ID"""
        ...

    @get(
        "/subscriptions/subpage-config/{shortUuid}",
        response_class=GetSubpageConfigByShortUuidResponseDto,
    )
    async def get_subpage_config(
        self,
        short_uuid: Annotated[
            Union[str, UUID],
            Path(description="Short UUID of the subscription", alias="shortUuid"),
        ],
        body: Annotated[GetSubpageConfigByShortUuidRequestBodyDto, PydanticBody()],
    ) -> GetSubpageConfigByShortUuidResponseDto:
        """Get subscription page config by short UUID"""
        ...

    @get(
        "/subscriptions/by-short-uuid/{shortUuid}/raw",
        response_class=GetRawSubscriptionByShortUuidResponseDto,
    )
    async def get_raw_subscription(
        self,
        short_uuid: Annotated[
            Union[str, UUID],
            Path(description="Short UUID of the user", alias="shortUuid"),
        ],
        with_disabled_hosts: Annotated[
            bool,
            Query(
                default=False,
                alias="withDisabledHosts",
                description="Include disabled hosts",
            ),
        ] = False,
    ) -> GetRawSubscriptionByShortUuidResponseDto:
        """None"""
        ...

    @get(
        "/subscriptions/connection-keys/{userId}",
        response_class=GetConnectionKeysByUserIdResponseDto,
    )
    async def get_connection_keys_by_user_id(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetConnectionKeysByUserIdResponseDto:
        """Get connection keys (base64 format) by user ID"""
        ...
