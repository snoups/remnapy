from typing import Annotated, List
from uuid import UUID

from rapid_api_client import PydanticBody

from remnapy.models import (
    UpdateManyHostsRequestDto,
)
from remnapy.rapid import AttributeBody, BaseController, patch, post


class HostsBulkActionsController(BaseController):
    @post("/hosts/bulk/delete", response_class=None)
    async def delete_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Delete many hosts"""
        ...

    @post("/hosts/bulk/disable", response_class=None)
    async def disable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Disable many hosts"""
        ...

    @post("/hosts/bulk/enable", response_class=None)
    async def enable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> None:
        """Enable many hosts"""
        ...

    @patch("/hosts/bulk/update", response_class=None)
    async def update_hosts(
        self,
        body: Annotated[UpdateManyHostsRequestDto, PydanticBody()],
    ) -> None:
        """Update many hosts"""
        ...
