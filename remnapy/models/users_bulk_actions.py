from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from remnapy.enums import TrafficLimitStrategy, UserStatus

# Type alias for tag validation
TagStr = Annotated[str, Field(min_length=1, max_length=16, pattern=r"^[A-Z0-9_]+$")]


# Request DTOs
class BulkDeleteUsersByStatusRequestDto(BaseModel):
    """Request to delete users by status"""

    status: UserStatus = Field(default=UserStatus.ACTIVE)


class BulkDeleteUsersRequestDto(BaseModel):
    """Request to delete users by IDs"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )


class BulkRevokeUsersSubscriptionRequestDto(BaseModel):
    """Request to revoke users subscription"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )


class BulkResetTrafficUsersRequestDto(BaseModel):
    """Request to reset traffic for users"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )


class UpdateUserFields(BaseModel):
    """Fields to update for users"""

    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[int] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited",
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy",
    )
    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z",
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters.",
    )
    hwid_device_limit: Optional[int] = Field(
        None, serialization_alias="hwidDeviceLimit", ge=0
    )
    external_squad_uuid: Optional[UUID] = Field(
        None,
        serialization_alias="externalSquadUuid",
        description="Optional. External squad UUID.",
    )


class BulkUpdateUsersRequestDto(BaseModel):
    """Request to bulk update users"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )
    fields: UpdateUserFields


class BulkUpdateUsersSquadsRequestDto(BaseModel):
    """Request to update users internal squads"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )
    active_internal_squads: list[UUID] = Field(
        serialization_alias="activeInternalSquads"
    )


class BulkExtendExpirationDateRequestDto(BaseModel):
    """Request to extend expiration date for selected users"""

    user_ids: list[int] = Field(
        serialization_alias="userIds",
        min_length=1,
        max_length=500,
    )
    extend_days: int = Field(serialization_alias="extendDays", ge=1, le=9999)


class BulkAllUpdateUsersRequestDto(BaseModel):
    """Request to update all users"""

    status: Optional[UserStatus] = Field(default=UserStatus.ACTIVE)
    traffic_limit_bytes: Optional[int] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited",
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy",
    )
    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z",
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters.",
    )
    hwid_device_limit: Optional[int] = Field(
        None, serialization_alias="hwidDeviceLimit", ge=0
    )


class BulkAllExtendExpirationDateRequestDto(BaseModel):
    """Request to extend expiration date for all users"""

    extend_days: int = Field(serialization_alias="extendDays", ge=1)


# Base Response DTOs (без обертки response)


# Response DTOs - наследуются от базовых


# Legacy compatibility
BulkUpdateUsersInternalSquadsRequestDto = BulkUpdateUsersSquadsRequestDto
