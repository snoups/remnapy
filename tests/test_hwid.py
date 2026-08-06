import uuid

import pytest

from remnapy.models import (
    CreateUserHwidDeviceRequestDto,
    CreateUserHwidDeviceResponseDto,
    DeleteUserAllHwidDeviceRequestDto,
    DeleteUserHwidDeviceRequestDto,
    DeleteUserHwidDeviceResponseDto,
    GetHwidStatisticsResponseDto,
    GetUserHwidDevicesResponseDto,
)
from tests.conftest import REMNAWAVE_USER_ID


class TestHwidInfo:
    """HWID device information"""

    @pytest.mark.asyncio
    async def test_get_hwid_user(self, remnawave):
        """Fetching HWID devices of a single user"""
        hwid = await remnawave.hwid.get_hwid_user(user_id=REMNAWAVE_USER_ID)
        assert isinstance(hwid, GetUserHwidDevicesResponseDto)
        assert hasattr(hwid, "devices")

    @pytest.mark.asyncio
    async def test_get_hwid_users(self, remnawave):
        """Fetching all HWID devices with pagination"""
        response = await remnawave.hwid.get_hwid_users(size=10, start=0)
        assert isinstance(response, GetUserHwidDevicesResponseDto)
        assert hasattr(response, "total")
        assert hasattr(response, "devices")


class TestHwidStatistics:
    """HWID device statistics"""

    @pytest.mark.asyncio
    async def test_get_hwid_stats(self, remnawave):
        """Fetching HWID device statistics"""
        try:
            response = await remnawave.hwid.get_hwid_stats()
            assert isinstance(response, GetHwidStatisticsResponseDto)

            assert hasattr(response, "by_platform")
            assert hasattr(response, "by_app")
            assert hasattr(response, "stats")

            assert hasattr(response.stats, "total_unique_devices")
            assert hasattr(response.stats, "total_hwid_devices")
            assert hasattr(response.stats, "average_hwid_devices_per_user")

            assert isinstance(response.stats.total_unique_devices, float)
            assert isinstance(response.stats.total_hwid_devices, float)
            assert isinstance(response.stats.average_hwid_devices_per_user, float)

            if len(response.by_platform) > 0:
                platform = response.by_platform[0]
                assert hasattr(platform, "platform")
                assert hasattr(platform, "count")

            if len(response.by_app) > 0:
                app = response.by_app[0]
                assert hasattr(app, "app")
                assert hasattr(app, "count")
        except Exception as e:
            pytest.skip(f"Skipping HWID stats test: {e!s}")


class TestHwidCRUD:
    """HWID device CRUD operations"""

    @pytest.fixture
    def test_hwid(self):
        """Generate a throwaway HWID."""
        return str(uuid.uuid4())

    @pytest.mark.asyncio
    # @pytest.mark.xfail(reason="User hwid device limit may be reached")
    async def test_add_hwid_to_user(self, remnawave, test_hwid):
        """Adding an HWID device to a user"""
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=test_hwid,
            user_id=REMNAWAVE_USER_ID,
            platform="Windows",
            os_version="10.0.19042",
            device_model="Surface Pro",
            user_agent="Mozilla/5.0",
        )

        response = await remnawave.hwid.add_hwid_to_users(body=create_request)

        assert isinstance(response, CreateUserHwidDeviceResponseDto)
        assert any(item.hwid == test_hwid for item in response.devices)

        hwid_check = await remnawave.hwid.get_hwid_user(user_id=REMNAWAVE_USER_ID)
        assert any(device.hwid == test_hwid for device in hwid_check.devices)

    @pytest.mark.asyncio
    async def test_delete_hwid_user(self, remnawave, test_hwid):
        """Deleting an HWID device from a user"""
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=test_hwid,
            user_id=REMNAWAVE_USER_ID,
            platform="Android",
            os_version="12",
            device_model="Pixel 6",
            user_agent="Chrome Mobile",
        )
        await remnawave.hwid.add_hwid_to_users(body=create_request)

        delete_request = DeleteUserHwidDeviceRequestDto(
            hwid=test_hwid, user_id=REMNAWAVE_USER_ID
        )
        response = await remnawave.hwid.delete_hwid_to_user(body=delete_request)

        assert isinstance(response, DeleteUserHwidDeviceResponseDto)
        assert not any(item.hwid == test_hwid for item in response.devices)

        hwid_check = await remnawave.hwid.get_hwid_user(user_id=REMNAWAVE_USER_ID)
        assert not any(device.hwid == test_hwid for device in hwid_check.devices)

    @pytest.mark.asyncio
    async def test_delete_all_hwid_user(self, remnawave):
        """Deleting all HWID devices of a user"""
        random_hwid = str(uuid.uuid4())
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=random_hwid,
            user_id=REMNAWAVE_USER_ID,
            platform="iOS",
            os_version="15.0",
            device_model="iPhone 13",
            user_agent="Safari/605.1.15",
        )
        await remnawave.hwid.add_hwid_to_users(body=create_request)

        check_before = await remnawave.hwid.get_hwid_user(user_id=REMNAWAVE_USER_ID)
        assert any(device.hwid == random_hwid for device in check_before.devices)

        delete_all_request = DeleteUserAllHwidDeviceRequestDto(
            user_id=REMNAWAVE_USER_ID
        )
        response = await remnawave.hwid.delete_all_hwid_user(body=delete_all_request)

        assert isinstance(response, DeleteUserHwidDeviceResponseDto)

        hwid_check = await remnawave.hwid.get_hwid_user(user_id=REMNAWAVE_USER_ID)
        assert not any(device.hwid == random_hwid for device in hwid_check.devices)
