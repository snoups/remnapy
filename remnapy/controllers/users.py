from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    CreateUserRequestDto,
    CreateUserResponseDto,
    DeleteUserResponseDto,
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
    ) -> GetAllUsersResponseDto:
        """Get all users"""
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
    ) -> GetUsersStreamResponseDto:
        """Get all users using cursor-based (keyset) pagination"""
        ...

    @delete("/users/{userId}", response_class=DeleteUserResponseDto)
    async def delete_user(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
    ) -> DeleteUserResponseDto:
        """Delete user"""
        ...

    @post(
        "/users/{userId}/actions/revoke", response_class=RevokeUserSubscriptionResponseDto
    )
    async def revoke_user_subscription(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
        body: Optional[Annotated[RevokeUserRequestDto, PydanticBody()]] = None,
    ) -> RevokeUserSubscriptionResponseDto:
        """Revoke User Subscription"""
        ...

    @post("/users/{userId}/actions/disable", response_class=DisableUserResponseDto)
    async def disable_user(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
    ) -> DisableUserResponseDto:
        """Disable User"""
        ...

    @post("/users/{userId}/actions/enable", response_class=EnableUserResponseDto)
    async def enable_user(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
    ) -> EnableUserResponseDto:
        """Enable User"""
        ...

    @post(
        "/users/{userId}/actions/reset-traffic",
        response_class=ResetUserTrafficResponseDto,
    )
    async def reset_user_traffic(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
    ) -> ResetUserTrafficResponseDto:
        """Reset User Traffic"""
        ...

    @post("/users/{userId}/actions/extend", response_class=ExtendUserResponseDto)
    async def extend_user(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
        body: Annotated[ExtendUserRequestDto, PydanticBody()],
    ) -> ExtendUserResponseDto:
        """Extend user expiration date"""
        ...

    @get("/users/{userId}", response_class=GetUserByIdResponseDto)
    async def get_user_by_id(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
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
        userId: Annotated[int, Path(description="ID of the user")],
    ) -> GetUserAccessibleNodesResponseDto:
        """Get user accessible nodes"""
        ...

    @get(
        "/users/{userId}/subscription-request-history",
        response_class=GetUserSubscriptionRequestHistoryResponseDto,
    )
    async def get_user_subscription_request_history(
        self,
        userId: Annotated[int, Path(description="ID of the user")],
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
