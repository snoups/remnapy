from typing import Annotated, Optional, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models import (
    AddManyUsersToInternalSquadRequestDto,
    AddManyUsersToInternalSquadResponseDto,
    AddUsersToInternalSquadRequestDto,
    AddUsersToInternalSquadResponseDto,
    CreateInternalSquadRequestDto,
    CreateInternalSquadResponseDto,
    DeleteInternalSquadResponseDto,
    DeleteManyUsersFromInternalSquadRequestDto,
    DeleteManyUsersFromInternalSquadResponseDto,
    DeleteUsersFromInternalSquadRequestDto,
    DeleteUsersFromInternalSquadResponseDto,
    GetAllInternalSquadsResponseDto,
    GetInternalSquadAccessibleNodesResponseDto,
    GetInternalSquadByUuidResponseDto,
    GetInternalSquadUsageResponseDto,
    ReorderInternalSquadsRequestDto,
    ReorderInternalSquadsResponseDto,
    UpdateInternalSquadRequestDto,
    UpdateInternalSquadResponseDto,
)
from remnapy.rapid import BaseController, delete, get, patch, post


class InternalSquadsController(BaseController):
    @get("/internal-squads", response_class=GetAllInternalSquadsResponseDto)
    async def get_internal_squads(self) -> GetAllInternalSquadsResponseDto:
        """Get all internal squads"""
        ...

    @post("/internal-squads", response_class=CreateInternalSquadResponseDto)
    async def create_internal_squad(
        self,
        body: Annotated[CreateInternalSquadRequestDto, PydanticBody()],
    ) -> CreateInternalSquadResponseDto:
        """Create internal squad"""
        ...

    @patch("/internal-squads", response_class=UpdateInternalSquadResponseDto)
    async def update_internal_squad(
        self,
        body: Annotated[UpdateInternalSquadRequestDto, PydanticBody()],
    ) -> UpdateInternalSquadResponseDto:
        """Update internal squad"""
        ...

    @get("/internal-squads/{uuid}", response_class=GetInternalSquadByUuidResponseDto)
    async def get_internal_squad_by_uuid(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> GetInternalSquadByUuidResponseDto:
        """Get internal squad by uuid"""
        ...

    @delete("/internal-squads/{uuid}", response_class=DeleteInternalSquadResponseDto)
    async def delete_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> DeleteInternalSquadResponseDto:
        """Delete internal squad"""
        ...

    @post(
        "/internal-squads/{uuid}/bulk-actions/add-users",
        response_class=AddUsersToInternalSquadResponseDto,
    )
    async def add_users_to_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> AddUsersToInternalSquadResponseDto:
        """Add users to internal squad"""
        ...

    @delete(
        "/internal-squads/{uuid}/bulk-actions/remove-users",
        response_class=DeleteUsersFromInternalSquadResponseDto,
    )
    async def remove_users_from_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> DeleteUsersFromInternalSquadResponseDto:
        """Delete users from internal squad"""
        ...

    @get(
        "/internal-squads/{uuid}/accessible-nodes",
        response_class=GetInternalSquadAccessibleNodesResponseDto,
    )
    async def get_accessible_nodes(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
    ) -> GetInternalSquadAccessibleNodesResponseDto:
        """Get accessible nodes for internal squad"""
        ...

    @post(
        "/internal-squads/actions/reorder",
        response_class=ReorderInternalSquadsResponseDto,
    )
    async def reorder_internal_squads(
        self,
        body: Annotated[ReorderInternalSquadsRequestDto, PydanticBody()],
    ) -> ReorderInternalSquadsResponseDto:
        """Reorder internal squads"""
        ...

    @get(
        "/internal-squads/{uuid}/usage",
        response_class=GetInternalSquadUsageResponseDto,
    )
    async def get_internal_squad_usage(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        min_total_bytes: Annotated[
            int,
            Query(
                default=0, ge=0, alias="minTotalBytes", description="Minimum total bytes"
            ),
        ] = 0,
        limit: Annotated[
            int,
            Query(
                default=250, ge=1, le=1000, description="Number of users to return"
            ),
        ] = 250,
        cursor: Annotated[
            Optional[int], Query(default=None, description="Pagination cursor")
        ] = None,
    ) -> GetInternalSquadUsageResponseDto:
        """Get internal squad usage"""
        ...

    @post(
        "/internal-squads/{uuid}/bulk-actions/add-many-users",
        response_class=AddManyUsersToInternalSquadResponseDto,
    )
    async def add_many_users_to_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        body: Annotated[AddManyUsersToInternalSquadRequestDto, PydanticBody()],
    ) -> AddManyUsersToInternalSquadResponseDto:
        """Add many users to internal squad"""
        ...

    @delete(
        "/internal-squads/{uuid}/bulk-actions/remove-many-users",
        response_class=DeleteManyUsersFromInternalSquadResponseDto,
    )
    async def remove_many_users_from_internal_squad(
        self,
        uuid: Annotated[
            Union[str, UUID], Path(description="UUID of the internal squad")
        ],
        body: Annotated[DeleteManyUsersFromInternalSquadRequestDto, PydanticBody()],
    ) -> DeleteManyUsersFromInternalSquadResponseDto:
        """Remove many users from internal squad"""
        ...
