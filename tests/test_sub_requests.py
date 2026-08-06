import pytest

from remnapy.models import (
    GetAllSubscriptionRequestHistoryResponseDto,
    GetSubscriptionRequestHistoryStatsResponseDto,
)


class TestSubscriptionRequestHistory:
    """Subscription request history"""

    @pytest.mark.asyncio
    async def test_get_all_subscription_request_history(self, remnawave):
        """Fetching the full subscription request history"""
        response = await remnawave.subscription_request_history.get_all_subscription_request_history(
            size=10, start=0
        )
        assert isinstance(response, GetAllSubscriptionRequestHistoryResponseDto)
        assert hasattr(response, "total")
        assert hasattr(response, "records")

    @pytest.mark.asyncio
    async def test_get_subscription_request_history_stats(self, remnawave):
        """Fetching subscription request history statistics"""
        response = await remnawave.subscription_request_history.get_subscription_request_history_stats()
        assert isinstance(response, GetSubscriptionRequestHistoryStatsResponseDto)
        assert hasattr(response, "by_parsed_app")
        assert hasattr(response, "hourly_request_stats")
