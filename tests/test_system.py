import pytest

from remnapy.models import (
    GetBandwidthStatsResponseDto,
    GetNodesMetricsResponseDto,
    GetNodesStatisticsResponseDto,
    GetRemnawaveHealthResponseDto,
    GetStatsResponseDto,
)


class TestSystemStatistics:
    """System statistics"""

    @pytest.mark.asyncio
    async def test_get_stats(self, remnawave):
        """Fetching overall statistics"""
        stats = await remnawave.system.get_stats()
        assert isinstance(stats, GetStatsResponseDto)
        assert hasattr(stats, "timestamp")
        assert hasattr(stats, "uptime")

    @pytest.mark.asyncio
    async def test_get_bandwidth_stats(self, remnawave):
        """Fetching bandwidth statistics"""
        bandwidth_stats = await remnawave.system.get_bandwidth_stats()
        assert isinstance(bandwidth_stats, GetBandwidthStatsResponseDto)
        assert hasattr(bandwidth_stats, "current_year")

    @pytest.mark.asyncio
    async def test_get_nodes_statistics(self, remnawave):
        """Fetching per-node statistics"""
        nodes_statistics = await remnawave.system.get_nodes_statistics()
        assert isinstance(nodes_statistics, GetNodesStatisticsResponseDto)
        assert hasattr(nodes_statistics, "last_seven_days")


class TestSystemMonitoring:
    """System monitoring"""

    @pytest.mark.asyncio
    async def test_get_nodes_metrics(self, remnawave):
        """Fetching node metrics"""
        nodes_metrics = await remnawave.system.get_nodes_metrics()
        assert isinstance(nodes_metrics, GetNodesMetricsResponseDto)
        assert hasattr(nodes_metrics, "nodes")
        assert isinstance(nodes_metrics.nodes, list)

        if nodes_metrics.nodes:
            node = nodes_metrics.nodes[0]
            assert hasattr(node, "uuid")
            assert hasattr(node, "name")
            assert hasattr(node, "cpu_usage")
            assert hasattr(node, "memory_usage")
            assert hasattr(node, "network_upload")
            assert hasattr(node, "network_download")
            assert hasattr(node, "uptime")
            assert hasattr(node, "last_seen")
            assert hasattr(node, "connected_users")

    @pytest.mark.asyncio
    async def test_get_health(self, remnawave):
        """Fetching system health"""
        health = await remnawave.system.get_health()
        assert isinstance(health, GetRemnawaveHealthResponseDto)
        assert hasattr(health, "runtime_metrics")
