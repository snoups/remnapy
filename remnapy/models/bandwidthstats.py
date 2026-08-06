from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, RootModel

# ============ Legacy Models (Deprecated) ============


class NodeUsageResponseDto(BaseModel):
    """Deprecated: Old node usage model"""

    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    total: int
    total_download: float = Field(alias="totalDownload")
    total_upload: float = Field(alias="totalUpload")
    human_readable_total: str = Field(alias="humanReadableTotal")
    human_readable_total_download: str = Field(alias="humanReadableTotalDownload")
    human_readable_total_upload: str = Field(alias="humanReadableTotalUpload")
    date: date


class NodesUsageResponseDto(RootModel[list[NodeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesUsageResponseDto instead"""

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        return bool(self.root)

    def __len__(self):
        return len(self.root)


class NodeRealtimeUsageResponseDto(BaseModel):
    """Deprecated: Use NodeRealtimeUsageItem instead"""

    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class NodesRealtimeUsageResponseDto(RootModel[list[NodeRealtimeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesRealtimeUsageResponseDto instead"""

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        return bool(self.root)

    def __len__(self):
        return len(self.root)


# ============ New Stats Models ============

# Realtime Stats


class NodeRealtimeUsageItem(BaseModel):
    """Node realtime usage item"""

    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class GetStatsNodesRealtimeUsageResponseDto(RootModel[list[NodeRealtimeUsageItem]]):
    """Response for nodes realtime usage"""

    @property
    def response(self) -> list[NodeRealtimeUsageItem]:
        return self.root

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# Stats Nodes Usage (with charts)


class TopNodeItem(BaseModel):
    """Top node item"""

    uuid: UUID
    color: str
    name: str
    country_code: str = Field(alias="countryCode")
    total: int


class NodeSeriesItem(BaseModel):
    """Node series item for charts"""

    uuid: UUID
    name: str
    color: str
    country_code: str = Field(alias="countryCode")
    total: int
    data: list[int]


class StatsNodesUsageData(BaseModel):
    """Stats nodes usage data"""

    categories: list[str]
    sparkline_data: list[int] = Field(alias="sparklineData")
    top_nodes: list[TopNodeItem] = Field(alias="topNodes")
    series: list[NodeSeriesItem]


class GetStatsNodesUsageResponseDto(RootModel[StatsNodesUsageData]):
    """Response for stats nodes usage"""

    @property
    def response(self) -> StatsNodesUsageData:
        return self.root


# Stats Node Users Usage (with charts)


class TopUserItem(BaseModel):
    """Top user item"""

    color: str
    username: str
    total: int


class StatsNodeUsersUsageData(BaseModel):
    """Stats node users usage data"""

    categories: list[str]
    sparkline_data: list[int] = Field(alias="sparklineData")
    top_users: list[TopUserItem] = Field(alias="topUsers")


class GetStatsNodeUsersUsageResponseDto(RootModel[StatsNodeUsersUsageData]):
    """Response for stats node users usage"""

    @property
    def response(self) -> StatsNodeUsersUsageData:
        return self.root


class GetStatsNodesUsersUsageRequestDto(BaseModel):
    """Request for stats users usage across multiple nodes"""

    nodes_uuids: list[UUID] = Field(serialization_alias="nodesUuids", min_length=1)


class GetStatsNodesUsersUsageResponseDto(RootModel[StatsNodeUsersUsageData]):
    """Response for stats users usage across multiple nodes"""

    @property
    def response(self) -> StatsNodeUsersUsageData:
        return self.root


# Stats User Usage (with charts)


class StatsUserUsageData(BaseModel):
    """Stats user usage data"""

    categories: list[str]
    sparkline_data: list[int] = Field(alias="sparklineData")
    top_nodes: list[TopNodeItem] = Field(alias="topNodes")
    series: list[NodeSeriesItem]


class GetStatsUserUsageResponseDto(RootModel[StatsUserUsageData]):
    """Response for stats user usage"""

    @property
    def response(self) -> StatsUserUsageData:
        return self.root


# Squad and node usage (3.2.1)


class SquadUserUsageNode(BaseModel):
    """Per-node traffic for a day"""

    uuid: UUID
    total_bytes: float = Field(alias="totalBytes")


class SquadUserUsageDay(BaseModel):
    """Daily traffic breakdown"""

    date: str
    nodes: list[SquadUserUsageNode]


class GetInternalSquadUserUsageResponseDto(BaseModel):
    """Response for GET /api/bandwidth-stats/internal-squads/{squadUuid}/users/{userId}/usage"""

    days: list[SquadUserUsageDay]


class GetNodesUsageRequestDto(BaseModel):
    """Request body for POST /api/bandwidth-stats/nodes/usage"""

    nodes_uuids: list[UUID] = Field(
        ...,
        serialization_alias="nodesUuids",
        description="Node UUIDs to aggregate over",
    )


class NodeUsageUser(BaseModel):
    """User traffic on a node"""

    id: int
    total_bytes: float = Field(alias="totalBytes")


class NodeUsageEntry(BaseModel):
    """Per-node user traffic list"""

    uuid: UUID
    users: list[NodeUsageUser]


class GetNodesUsageResponseDto(BaseModel):
    """Response for POST /api/bandwidth-stats/nodes/usage"""

    nodes: list[NodeUsageEntry]
