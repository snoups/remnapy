from typing import Annotated, Optional, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models.bandwidthstats import (
    GetInternalSquadUserUsageResponseDto,
    GetNodesUsageByRangeResponseDto,
    GetNodesUsageRequestDto,
    GetNodesUsageResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodesUsersUsageRequestDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
)
from remnapy.models.internal_squads import GetInternalSquadUsageResponseDto
from remnapy.rapid import BaseController, get, post


class BandWidthStatsController(BaseController):
    # ============ New Stats Endpoints ============

    @get(
        "/bandwidth-stats/nodes/{uuid}/users",
        response_class=GetStatsNodeUsersUsageResponseDto,
    )
    async def get_stats_node_users_usage(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="UUID of the node")],
        top_users_limit: Annotated[
            int,
            Query(description="Limit of top users to return", alias="topUsersLimit"),
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetStatsNodeUsersUsageResponseDto:
        """Get Node Users Usage by Node UUID"""
        ...

    @get("/bandwidth-stats/users/{uuid}", response_class=GetStatsUserUsageResponseDto)
    async def get_stats_user_usage(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="UUID of the user")],
        top_nodes_limit: Annotated[
            int,
            Query(description="Limit of top nodes to return", alias="topNodesLimit"),
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetStatsUserUsageResponseDto:
        """Get User Usage by Range"""
        ...

    @get("/bandwidth-stats/nodes", response_class=GetStatsNodesUsageResponseDto)
    async def get_stats_nodes_usage(
        self,
        top_nodes_limit: Annotated[
            int,
            Query(description="Limit of top nodes to return", alias="topNodesLimit"),
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetStatsNodesUsageResponseDto:
        """Get Nodes Usage by Range"""
        ...

    @post(
        "/bandwidth-stats/nodes/users",
        response_class=GetStatsNodesUsersUsageResponseDto,
    )
    async def get_stats_nodes_users_usage(
        self,
        body: Annotated[GetStatsNodesUsersUsageRequestDto, PydanticBody()],
    ) -> GetStatsNodesUsersUsageResponseDto:
        """Get Nodes Users Usage by Nodes UUIDs"""
        ...

    @get(
        "/bandwidth-stats/internal-squads/{uuid}/usage",
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

    @get(
        "/bandwidth-stats/internal-squads/{squadUuid}/users/{userId}/usage",
        response_class=GetInternalSquadUserUsageResponseDto,
    )
    async def get_internal_squad_user_usage(
        self,
        squad_uuid: Annotated[
            Union[str, UUID],
            Path(description="UUID of the internal squad", alias="squadUuid"),
        ],
        user_id: Annotated[int, Path(description="ID of the user", alias="userId")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetInternalSquadUserUsageResponseDto:
        """Get internal squad user usage"""
        ...

    @post(
        "/bandwidth-stats/nodes/usage",
        response_class=GetNodesUsageResponseDto,
    )
    async def get_nodes_usage(
        self,
        body: Annotated[GetNodesUsageRequestDto, PydanticBody()],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        min_total_bytes: Annotated[
            int,
            Query(
                default=0, ge=0, alias="minTotalBytes", description="Minimum total bytes"
            ),
        ] = 0,
    ) -> GetNodesUsageResponseDto:
        """Get nodes usage by node UUIDs"""
        ...
