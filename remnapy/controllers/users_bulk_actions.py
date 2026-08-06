from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    BulkAllExtendExpirationDateRequestDto,
    BulkAllUpdateUsersRequestDto,
    BulkDeleteUsersByStatusRequestDto,
    BulkDeleteUsersRequestDto,
    BulkExtendExpirationDateRequestDto,
    BulkResetTrafficUsersRequestDto,
    BulkRevokeUsersSubscriptionRequestDto,
    BulkUpdateUsersRequestDto,
    BulkUpdateUsersSquadsRequestDto,
)
from remnapy.rapid import BaseController, post


class UsersBulkActionsController(BaseController):
    @post(
        "/users/bulk/delete-by-status",
        response_class=None,
    )
    async def bulk_delete_users_by_status(
        self, body: Annotated[BulkDeleteUsersByStatusRequestDto, PydanticBody()]
    ) -> None:
        """Bulk Delete Users By Status"""
        ...

    @post("/users/bulk/delete", response_class=None)
    async def bulk_delete_users(
        self,
        body: Annotated[BulkDeleteUsersRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Delete Users By UUIDs"""
        ...

    @post(
        "/users/bulk/revoke-subscription",
        response_class=None,
    )
    async def bulk_revoke_users_subscription(
        self,
        body: Annotated[BulkRevokeUsersSubscriptionRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Revoke Users Subscription"""
        ...

    @post("/users/bulk/reset-traffic", response_class=None)
    async def bulk_reset_user_traffic(
        self,
        body: Annotated[BulkResetTrafficUsersRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Reset User Traffic"""
        ...

    @post("/users/bulk/update", response_class=None)
    async def bulk_update_users(
        self,
        body: Annotated[BulkUpdateUsersRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Update Users"""
        ...

    @post("/users/bulk/update-squads", response_class=None)
    async def bulk_update_users_internal_squads(
        self,
        body: Annotated[BulkUpdateUsersSquadsRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Update Users Internal Squads"""
        ...

    @post(
        "/users/bulk/extend-expiration-date",
        response_class=None,
    )
    async def bulk_extend_expiration_date(
        self,
        body: Annotated[BulkExtendExpirationDateRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Extend Users Expiration Date"""
        ...

    @post("/users/bulk/all/update", response_class=None)
    async def bulk_update_all_users(
        self,
        body: Annotated[BulkAllUpdateUsersRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Update All Users"""
        ...

    @post(
        "/users/bulk/all/reset-traffic",
        response_class=None,
    )
    async def bulk_all_reset_user_traffic(
        self,
    ) -> None:
        """Bulk Reset All Users Traffic"""
        ...

    @post(
        "/users/bulk/all/extend-expiration-date",
        response_class=None,
    )
    async def bulk_all_extend_expiration_date(
        self,
        body: Annotated[BulkAllExtendExpirationDateRequestDto, PydanticBody()],
    ) -> None:
        """Bulk Extend All Users Expiration Date"""
        ...
