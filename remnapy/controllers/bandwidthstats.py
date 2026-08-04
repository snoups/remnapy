from typing import Annotated, Optional, Union
from uuid import UUID

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnapy.models.bandwidthstats import (
    GetInternalSquadUserUsageResponseDto,
    GetLegacyStatsNodesUsersUsageResponseDto,
    GetLegacyStatsUserUsageResponseDto,
    GetNodesUsageByRangeResponseDto,
    GetNodesUsageRequestDto,
    GetNodesUsageResponseDto,
    GetNodeUserUsageByRangeResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodesUsersUsageRequestDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
    GetUserUsageByRangeResponseDto,
)
from remnapy.models.internal_squads import GetInternalSquadUsageResponseDto
from remnapy.rapid import BaseController, get, post


class BandWidthStatsController(BaseController):
    # ============ Legacy Endpoints (Deprecated) ============

    @get(
        "/bandwidth-stats/users/{userUuid}/legacy",
        response_class=GetUserUsageByRangeResponseDto,
    )
    async def get_user_usage_legacy_old(
        self,
        user_uuid: Annotated[
            str, Path(description="UUID of the user", alias="userUuid")
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetUserUsageByRangeResponseDto:
        """Get User Usage by Range (Legacy - Deprecated)"""
        ...

    @get(
        "/bandwidth-stats/nodes/{nodeUuid}/users/legacy",
        response_class=GetNodeUserUsageByRangeResponseDto,
    )
    async def get_node_user_usage_legacy_old(
        self,
        node_uuid: Annotated[
            str, Path(description="UUID of the node", alias="nodeUuid")
        ],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetNodeUserUsageByRangeResponseDto:
        """Get Node User Usage by Range and Node UUID (Legacy - Deprecated)"""
        ...

    # ============ New Stats Endpoints ============

    @get(
        "/bandwidth-stats/nodes/{uuid}/users/legacy",
        response_class=GetLegacyStatsNodesUsersUsageResponseDto,
    )
    async def get_node_users_usage_legacy_stats(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="UUID of the node")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetLegacyStatsNodesUsersUsageResponseDto:
        """Get Node Users Usage by Range and Node UUID (Legacy Stats)"""
        ...

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

    @get(
        "/bandwidth-stats/users/{uuid}/legacy",
        response_class=GetLegacyStatsUserUsageResponseDto,
    )
    async def get_user_usage_legacy_stats(
        self,
        uuid: Annotated[Union[str, UUID], Path(description="UUID of the user")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetLegacyStatsUserUsageResponseDto:
        """Get User Usage by Range (Legacy Stats)"""
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
            Optional[float],
            Query(default=None, alias="minTotalBytes", description="Minimum total bytes"),
        ] = None,
        limit: Annotated[
            Optional[int], Query(default=None, description="Number of users to return")
        ] = None,
        cursor: Annotated[
            Optional[str], Query(default=None, description="Pagination cursor")
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
            Optional[float],
            Query(default=None, alias="minTotalBytes", description="Minimum total bytes"),
        ] = None,
    ) -> GetNodesUsageResponseDto:
        """Get nodes usage by node UUIDs"""
        ...
