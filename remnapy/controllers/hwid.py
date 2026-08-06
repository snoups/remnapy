from typing import Annotated, Optional

from rapid_api_client import Path, PydanticBody, Query

from remnapy.models import (
    CreateHWIDUser,
    CreateUserHwidDeviceResponseDto,
    DeleteUserAllHwidDeviceRequestDto,
    DeleteUserHwidDeviceResponseDto,
    GetHwidStatisticsResponseDto,
    GetTopUsersByHwidDevicesResponseDto,
    GetUserHwidDevicesResponseDto,
    HWIDDeleteRequest,
    TableFilter,
    TableSort,
)
from remnapy.rapid import BaseController, get, post


class HWIDUserController(BaseController):
    @get("/hwid/devices", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_users(
        self,
        size: Annotated[
            Optional[int],
            Query(
                default=None,
                description="Number of results to return, no more than 1000",
            ),
        ] = None,
        start: Annotated[
            Optional[int],
            Query(
                default=None,
                description="Start index (offset) of the results to return, default is 0",
            ),
        ] = None,
        filters: Annotated[
            Optional[list[TableFilter]],
            Query(default=None, description="Column filters"),
        ] = None,
        filter_modes: Annotated[
            Optional[dict[str, str]],
            Query(
                default=None, alias="filterModes", description="Per-column filter modes"
            ),
        ] = None,
        global_filter_mode: Annotated[
            Optional[str],
            Query(
                default=None, alias="globalFilterMode", description="Global filter mode"
            ),
        ] = None,
        sorting: Annotated[
            Optional[list[TableSort]],
            Query(default=None, description="Sort order"),
        ] = None,
    ) -> GetUserHwidDevicesResponseDto:
        """Get all user HWID devices"""
        ...

    @get("/hwid/devices/stats", response_class=GetHwidStatisticsResponseDto)
    async def get_hwid_stats(
        self,
    ) -> GetHwidStatisticsResponseDto:
        """Get HWID statistics"""
        ...

    @post("/hwid/devices", response_class=CreateUserHwidDeviceResponseDto)
    async def add_hwid_to_users(
        self,
        body: Annotated[CreateHWIDUser, PydanticBody()],
    ) -> CreateUserHwidDeviceResponseDto:
        """Create a user HWID device"""
        ...

    @post("/hwid/devices/delete", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_hwid_to_user(
        self,
        body: Annotated[HWIDDeleteRequest, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete a user HWID device"""
        ...

    @post("/hwid/devices/delete-all", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_all_hwid_user(
        self,
        body: Annotated[DeleteUserAllHwidDeviceRequestDto, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete all user HWID devices"""
        ...

    @get("/hwid/devices/{userId}", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_user(
        self,
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
    ) -> GetUserHwidDevicesResponseDto:
        """Get a user HWID device"""
        ...

    @get("/hwid/devices/top-users", response_class=GetTopUsersByHwidDevicesResponseDto)
    async def get_top_users_by_hwid_devices(
        self,
        size: Annotated[
            Optional[int], Query(default=None, description="Page size for pagination")
        ] = None,
        start: Annotated[
            Optional[int], Query(default=None, description="Offset for pagination")
        ] = None,
    ) -> GetTopUsersByHwidDevicesResponseDto:
        """Get top users by HWID devices"""
        ...
