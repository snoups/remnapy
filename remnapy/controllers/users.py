from typing import Annotated, Dict, List, Optional, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.enums import TrafficLimitStrategy, UserStatus
from remnapy.models import (
    CreateUserRequestDto,
    CreateUserResponseDto,
    DisableUserResponseDto,
    EnableUserResponseDto,
    ExtendUserRequestDto,
    ExtendUserResponseDto,
    GetAllTagsResponseDto,
    GetAllUsersResponseDto,
    GetUserAccessibleNodesResponseDto,
    GetUserByIdResponseDto,
    GetUserByShortUuidResponseDto,
    GetUserByUsernameResponseDto,
    GetUserSubscriptionRequestHistoryResponseDto,
    GetUsersStreamResponseDto,
    ResetUserTrafficResponseDto,
    ResolveUserRequestBodyDto,
    ResolveUserResponseDto,
    RevokeUserRequestDto,
    RevokeUserSubscriptionResponseDto,
    TableFilter,
    TableSort,
    UpdateUserRequestDto,
    UpdateUserResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class UsersController(BaseController):
    @post("/users", response_class=CreateUserResponseDto)
    async def create_user(
        self,
        body: Annotated[CreateUserRequestDto, PydanticBody()],
    ) -> CreateUserResponseDto:
        """Create a new user"""
        ...

    @patch("/users", response_class=UpdateUserResponseDto)
    async def update_user(
        self,
        body: Annotated[UpdateUserRequestDto, PydanticBody()],
    ) -> UpdateUserResponseDto:
        """Update a user by ID or username"""
        ...

    @get("/users", response_class=GetAllUsersResponseDto)
    async def get_all_users(
        self,
        start: Annotated[
            Optional[int], Query(default=None, description="Offset for pagination")
        ] = None,
        size: Annotated[
            Optional[int], Query(default=None, description="Page size for pagination")
        ] = None,
        filters: Annotated[
            Optional[List[TableFilter]],
            Query(default=None, description="Column filters"),
        ] = None,
        filter_modes: Annotated[
            Optional[Dict[str, str]],
            Query(default=None, alias="filterModes", description="Per-column filter modes"),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(default=None, alias="globalFilterMode", description="Global filter mode"),
        ] = None,
        sorting: Annotated[
            Optional[List[TableSort]],
            Query(default=None, description="Sort order"),
        ] = None,
    ) -> GetAllUsersResponseDto:
        """Get all users using offset-based pagination.

        `filters`/`filter_modes`/`global_filter_mode`/`sorting` mirror the
        panel's TanStack Table controls; per the spec, they are primarily
        intended for the frontend and rely on expensive `LIKE`-style
        operators server-side.
        """
        ...

    @get("/users/stream", response_class=GetUsersStreamResponseDto)
    async def get_users_stream(
        self,
        size: Annotated[
            Optional[int], Query(default=None, description="Page size")
        ] = None,
        cursor: Annotated[
            Optional[int],
            Query(
                default=None,
                description=(
                    "Keyset pagination cursor; pass the previous response's "
                    "nextCursor converted to an integer"
                ),
            ),
        ] = None,
        status: Annotated[
            Optional[UserStatus],
            Query(default=None, description="Status to filter users by"),
        ] = None,
        telegram_id: Annotated[
            Optional[str],
            Query(default=None, alias="telegramId", description="Telegram ID to filter users by"),
        ] = None,
        email: Annotated[
            Optional[str],
            Query(default=None, description="Email to filter users by"),
        ] = None,
        tag: Annotated[
            Optional[str],
            Query(default=None, description="Tag to filter users by"),
        ] = None,
        traffic_limit_strategy: Annotated[
            Optional[TrafficLimitStrategy],
            Query(
                default=None,
                alias="trafficLimitStrategy",
                description="Traffic limit strategy to filter users by",
            ),
        ] = None,
        external_squad_uuid: Annotated[
            Optional[Union[str, UUID]],
            Query(
                default=None,
                alias="externalSquadUuid",
                description="External squad UUID to filter users by",
            ),
        ] = None,
    ) -> GetUsersStreamResponseDto:
        """Get all users using cursor-based (keyset) pagination"""
        ...

    @delete("/users/{userId}", response_class=None)
    async def delete_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> None:
        """Delete user"""
        ...

    @post(
        "/users/{userId}/actions/revoke", response_class=RevokeUserSubscriptionResponseDto
    )
    async def revoke_user_subscription(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
        body: Optional[Annotated[RevokeUserRequestDto, PydanticBody()]] = None,
    ) -> RevokeUserSubscriptionResponseDto:
        """Revoke User Subscription"""
        ...

    @post("/users/{userId}/actions/disable", response_class=DisableUserResponseDto)
    async def disable_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> DisableUserResponseDto:
        """Disable User"""
        ...

    @post("/users/{userId}/actions/enable", response_class=EnableUserResponseDto)
    async def enable_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> EnableUserResponseDto:
        """Enable User"""
        ...

    @post(
        "/users/{userId}/actions/reset-traffic",
        response_class=ResetUserTrafficResponseDto,
    )
    async def reset_user_traffic(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> ResetUserTrafficResponseDto:
        """Reset User Traffic"""
        ...

    @post("/users/{userId}/actions/extend", response_class=ExtendUserResponseDto)
    async def extend_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
        body: Annotated[ExtendUserRequestDto, PydanticBody()],
    ) -> ExtendUserResponseDto:
        """Extend user expiration date"""
        ...

    @get("/users/{userId}", response_class=GetUserByIdResponseDto)
    async def get_user_by_id(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserByIdResponseDto:
        """Get user by ID"""
        ...

    @get("/users/tags", response_class=GetAllTagsResponseDto)
    async def get_all_tags(
        self,
    ) -> GetAllTagsResponseDto:
        """Get all existing user tags"""
        ...

    @get(
        "/users/{userId}/accessible-nodes",
        response_class=GetUserAccessibleNodesResponseDto,
    )
    async def get_user_accessible_nodes(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserAccessibleNodesResponseDto:
        """Get user accessible nodes"""
        ...

    @get(
        "/users/{userId}/subscription-request-history",
        response_class=GetUserSubscriptionRequestHistoryResponseDto,
    )
    async def get_user_subscription_request_history(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserSubscriptionRequestHistoryResponseDto:
        """Get user subscription request history, recent 24 records"""
        ...

    # ИСПРАВЛЕНО: убран alias, используется short_uuid
    @get(
        "/users/by-short-uuid/{shortUuid}", response_class=GetUserByShortUuidResponseDto
    )
    async def get_user_by_short_uuid(
        self,
        short_uuid: Annotated[
            str, Path(description="Short UUID of the user", alias="shortUuid")
        ],
    ) -> GetUserByShortUuidResponseDto:
        """Get user by Short UUID"""
        ...

    @get("/users/by-username/{username}", response_class=GetUserByUsernameResponseDto)
    async def get_user_by_username(
        self,
        username: Annotated[str, Path(description="Username of the user")],
    ) -> GetUserByUsernameResponseDto:
        """Get user by username"""
        ...

    @post("/users/resolve", response_class=ResolveUserResponseDto)
    async def resolve_user(
        self,
        body: Annotated[ResolveUserRequestBodyDto, PydanticBody()],
    ) -> ResolveUserResponseDto:
        """Resolve user by any identifier (id, shortUuid, username)"""
        ...
