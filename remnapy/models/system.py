import datetime
from typing import Optional

from pydantic import BaseModel, Field

from remnapy.enums import ResponseType
from remnapy.models.subscriptions_settings import ResponseRule, ResponseRules


class NodeStatistic(BaseModel):
    node_name: str = Field(alias="nodeName")
    date: datetime.date
    total_bytes: str = Field(alias="totalBytes")


class NodesStatisticResponseDto(BaseModel):
    last_seven_days: list[NodeStatistic] = Field(alias="lastSevenDays")


class BandwidthStatistic(BaseModel):
    current: str
    previous: str
    difference: str


class BandwidthStatisticResponseDto(BaseModel):
    last_two_days: BandwidthStatistic = Field(alias="bandwidthLastTwoDays")
    last_seven_days: BandwidthStatistic = Field(alias="bandwidthLastSevenDays")
    last_30_days: BandwidthStatistic = Field(alias="bandwidthLast30Days")
    calendar_month: BandwidthStatistic = Field(alias="bandwidthCalendarMonth")
    current_year: BandwidthStatistic = Field(alias="bandwidthCurrentYear")


class CPUStatistic(BaseModel):
    cores: float


class MemoryStatistic(BaseModel):
    total: float
    free: float
    used: float


class StatusCounts(BaseModel):
    """Dynamic status counts (additionalProperties in the spec)"""

    model_config = {"extra": "allow"}

    def __getitem__(self, key: str) -> int:
        """Allow dict-like access"""
        return getattr(self, key, 0)

    def get(self, key: str, default: int = 0) -> int:
        """Dict-like get method"""
        return getattr(self, key, default)


class UsersStatistic(BaseModel):
    status_counts: StatusCounts = Field(alias="statusCounts")
    total_users: float = Field(alias="totalUsers")


class OnlineStatistic(BaseModel):
    last_day: float = Field(alias="lastDay")
    last_week: float = Field(alias="lastWeek")
    never_online: float = Field(alias="neverOnline")
    online_now: float = Field(alias="onlineNow")


class NodesStatistic(BaseModel):
    total_online: float = Field(alias="totalOnline")
    total_bytes_lifetime: str = Field(alias="totalBytesLifetime")


class StatisticResponseDto(BaseModel):
    """System statistics data"""

    cpu: CPUStatistic
    memory: MemoryStatistic
    uptime: float
    timestamp: float
    users: UsersStatistic
    online_stats: OnlineStatistic = Field(alias="onlineStats")
    nodes: NodesStatistic


class PM2Stat(BaseModel):
    name: str
    memory: str
    cpu: str


class RemnawaveHealthData(BaseModel):
    pm2_stats: list[PM2Stat] = Field(alias="pm2Stats")


class GetStatsResponseDto(StatisticResponseDto):
    """Get system statistics response"""

    pass


class GetBandwidthStatsResponseDto(BaseModel):
    last_two_days: BandwidthStatistic = Field(alias="bandwidthLastTwoDays")
    last_seven_days: BandwidthStatistic = Field(alias="bandwidthLastSevenDays")
    last_30_days: BandwidthStatistic = Field(alias="bandwidthLast30Days")
    calendar_month: BandwidthStatistic = Field(alias="bandwidthCalendarMonth")
    current_year: BandwidthStatistic = Field(alias="bandwidthCurrentYear")


class GetNodesStatisticsResponseDto(BaseModel):
    last_seven_days: list[NodeStatistic] = Field(alias="lastSevenDays")


class RuntimeMetric(BaseModel):
    """Runtime metric from health endpoint"""

    model_config = {"extra": "allow"}

    rss: Optional[float] = None
    heap_total: Optional[float] = Field(None, alias="heapTotal")
    heap_used: Optional[float] = Field(None, alias="heapUsed")
    external: Optional[float] = None
    array_buffers: Optional[float] = Field(None, alias="arrayBuffers")
    event_loop_delay_ms: Optional[float] = Field(None, alias="eventLoopDelayMs")
    event_loop_p99_ms: Optional[float] = Field(None, alias="eventLoopP99Ms")
    active_handles: Optional[float] = Field(None, alias="activeHandles")
    uptime: Optional[float] = None
    pid: Optional[float] = None
    timestamp: Optional[float] = None
    instance_id: Optional[str] = Field(None, alias="instanceId")
    instance_type: Optional[str] = Field(None, alias="instanceType")


class GetRemnawaveHealthResponseDto(BaseModel):
    runtime_metrics: list[RuntimeMetric] = Field(
        default_factory=list, alias="runtimeMetrics"
    )


class TrafficStatDto(BaseModel):
    tag: str
    upload: str
    download: str


class NodeMetric(BaseModel):
    """Node metric data (API v1.10)"""

    node_uuid: str = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_emoji: str = Field(alias="countryEmoji")
    provider_name: str = Field(alias="providerName")
    users_online: float = Field(alias="usersOnline")
    inbounds_stats: list[TrafficStatDto] = Field(alias="inboundsStats")
    outbounds_stats: list[TrafficStatDto] = Field(alias="outboundsStats")

    @property
    def uuid(self) -> str:
        return self.node_uuid

    @property
    def name(self) -> str:
        return self.node_name

    @property
    def connected_users(self) -> float:
        return self.users_online

    @property
    def cpu_usage(self) -> None:
        return None

    @property
    def memory_usage(self) -> None:
        return None

    @property
    def network_upload(self) -> None:
        return None

    @property
    def network_download(self) -> None:
        return None

    @property
    def uptime(self) -> None:
        return None

    @property
    def last_seen(self) -> None:
        return None


class GetNodesMetricsResponseDto(BaseModel):
    nodes: list[NodeMetric]


class X25519KeyPair(BaseModel):
    public_key: str = Field(alias="publicKey")
    private_key: str = Field(alias="privateKey")


class GetX25519KeyPairResponseDto(BaseModel):
    key_pairs: list[X25519KeyPair] = Field(alias="keypairs")


# OpenAPI v1.10 schema name
GenerateX25519ResponseDto = GetX25519KeyPairResponseDto


class EncryptHappCryptoLinkRequestDto(BaseModel):
    link_to_encrypt: str = Field(serialization_alias="linkToEncrypt")


class EncryptHappCryptoLinkData(BaseModel):
    encrypted_link: str = Field(alias="encryptedLink")


class EncryptHappCryptoLinkResponseDto(EncryptHappCryptoLinkData):
    pass


class DebugSrrMatcherRequestDto(BaseModel):
    response_rules: ResponseRules = Field(serialization_alias="responseRules")


class DebugSrrMatcherData(BaseModel):
    matched: bool
    response_type: ResponseType = Field(alias="responseType")
    matched_rule: Optional[ResponseRule] = Field(alias="matchedRule")
    input_headers: dict[str, str] = Field(alias="inputHeaders")
    output_headers: dict[str, str] = Field(alias="outputHeaders")


class DebugSrrMatcherResponseDto(DebugSrrMatcherData):
    pass


class RecapThisMonth(BaseModel):
    users: float
    traffic: str


class RecapTotal(BaseModel):
    users: float
    nodes: float
    traffic: str
    nodes_ram: str = Field(alias="nodesRam")
    nodes_cpu_cores: float = Field(alias="nodesCpuCores")
    distinct_countries: float = Field(alias="distinctCountries")


class GetRecapResponseDto(BaseModel):
    this_month: RecapThisMonth = Field(alias="thisMonth")
    total: RecapTotal
    version: str
    init_date: datetime.datetime = Field(alias="initDate")


class BuildInfo(BaseModel):
    """Build information"""

    time: str
    number: str


class GitBackendInfo(BaseModel):
    """Git backend information"""

    commit_sha: str = Field(alias="commitSha")
    branch: str
    commit_url: str = Field(alias="commitUrl")


class GitFrontendInfo(BaseModel):
    """Git frontend information"""

    commit_sha: str = Field(alias="commitSha")
    commit_url: str = Field(alias="commitUrl")


class GitInfo(BaseModel):
    """Git information"""

    backend: GitBackendInfo
    frontend: GitFrontendInfo


class MetadataResponse(BaseModel):
    """Metadata response data"""

    version: str
    build: BuildInfo
    git: GitInfo


class GetMetadataResponseDto(MetadataResponse):
    """Get metadata response"""

    pass


class ConfigurationNotifications(BaseModel):
    """Webhook and notification thresholds"""

    webhook: bool
    bandwidth_usage: Optional[list[float]] = Field(alias="bandwidthUsage")
    not_connected_after: Optional[list[float]] = Field(alias="notConnectedAfter")
    expiration_notifications: Optional[list[float]] = Field(
        alias="expirationNotifications"
    )


class ConfigurationService(BaseModel):
    """Service-level toggles"""

    clean_usage_history: bool = Field(alias="cleanUsageHistory")
    disable_user_usage_records: bool = Field(alias="disableUserUsageRecords")
    disable_srh_records: bool = Field(alias="disableSrhRecords")
    export_to_redis_stream: bool = Field(alias="exportToRedisStream")


class ConfigurationMisc(BaseModel):
    """Miscellaneous panel configuration"""

    short_uuid_length: int = Field(alias="shortUuidLength")
    sub_public_domain: str = Field(alias="subPublicDomain")
    user_usage_ignore_below_bytes: float = Field(alias="userUsageIgnoreBelowBytes")


class GetConfigurationResponseDto(BaseModel):
    """Response for GET /api/system/configuration"""

    notifications: ConfigurationNotifications
    service: ConfigurationService
    misc: ConfigurationMisc


class StatsDigestUsers(BaseModel):
    """User counters for the digest period"""

    created_count: float = Field(alias="createdCount")
    expired_count: float = Field(alias="expiredCount")


class StatsDigestTraffic(BaseModel):
    """Traffic counters for the digest period"""

    total_bytes: str = Field(alias="totalBytes")
    by_users_created_in_range_bytes: str = Field(alias="byUsersCreatedInRangeBytes")


class StatsDigestHwidDevices(BaseModel):
    """HWID device counters for the digest period"""

    created_count: float = Field(alias="createdCount")


class GetStatsDigestResponseDto(BaseModel):
    """Response for GET /api/system/stats/digest"""

    users: StatsDigestUsers
    traffic: StatsDigestTraffic
    hwid_devices: StatsDigestHwidDevices = Field(alias="hwidDevices")


class HttpStatsRoute(BaseModel):
    """Request counter for a single route"""

    method: str
    route: str
    count: int


class GetHttpStatsResponseDto(BaseModel):
    """Response for GET /api/system/stats/http"""

    routes: list[HttpStatsRoute]
    total: int
