import random
from datetime import datetime, timedelta

import pytest
import pytz

from remnapy.enums import ErrorCode, UserStatus
from remnapy.exceptions import ApiError
from remnapy.models import (
    CreateUserRequestDto,
    GetSubscriptionRequestsResponseDto,
    GetUserAccessibleNodesResponseDto,
    RevokeUserRequestDto,
    TagsResponseDto,
    UpdateUserRequestDto,
    UserResponseDto,
    UsersResponseDto,
)
from remnapy.models.users import GetUserSubscriptionRequestHistoryResponseDto
from tests.utils import generate_email, generate_random_string


class TestUsersCRUD:
    """Тесты базовых CRUD операций для пользователей"""

    @pytest.mark.asyncio
    async def test_create_user(self, remnawave):
        email: str = generate_email(length=8)
        username: str = generate_random_string(length=8)
        telegram_id: int = random.randint(100000000, 999999999)
        expire_at: datetime = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserRequestDto(
                username=username,
                email=email,
                telegram_id=telegram_id,
                expire_at=expire_at,
            )
        )

        assert isinstance(create_user, UserResponseDto)
        assert create_user.username == username
        assert create_user.email == email
        assert create_user.telegram_id == telegram_id
        assert create_user.expire_at.isoformat(
            timespec="seconds"
        ) == expire_at.isoformat(timespec="seconds")

        # Clean up - delete the test user
        await remnawave.users.delete_user(user_id=create_user.id)

    @pytest.mark.asyncio
    async def test_update_user(self, remnawave):
        # Create test user first
        username: str = generate_random_string(length=8)
        expire_at: datetime = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserRequestDto(
                username=username,
                expire_at=expire_at,
            )
        )

        # Update user
        update_description: str = "TEST"
        update_status: UserStatus = UserStatus.DISABLED
        update_user = await remnawave.users.update_user(
            UpdateUserRequestDto(
                id=create_user.id,
                status=update_status,
                description=update_description,
            )
        )
        assert isinstance(update_user, UserResponseDto)
        assert update_user.id == create_user.id
        assert update_user.status == update_status
        assert update_user.description == update_description

        # Clean up
        await remnawave.users.delete_user(user_id=create_user.id)

    @pytest.mark.asyncio
    async def test_delete_user(self, remnawave):
        # Create test user first
        username: str = generate_random_string(length=8)
        expire_at: datetime = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserRequestDto(
                username=username,
                expire_at=expire_at,
            )
        )

        # Delete user
        delete_user = await remnawave.users.delete_user(user_id=create_user.id)
        assert delete_user is None
        assert delete_user is None


class TestUsersFetch:
    """Тесты получения информации о пользователях"""

    @pytest.mark.asyncio
    async def test_get_all_users(self, remnawave):
        all_users = await remnawave.users.get_all_users()
        assert isinstance(all_users, UsersResponseDto)

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, remnawave, test_user):
        user_by_id = await remnawave.users.get_user_by_id(user_id=test_user.id)
        assert isinstance(user_by_id, UserResponseDto)
        assert user_by_id.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_user_by_short_uuid(self, remnawave, test_user):
        user_short_uuid = await remnawave.users.get_user_by_short_uuid(
            short_uuid=test_user.short_uuid
        )
        assert isinstance(user_short_uuid, UserResponseDto)
        assert user_short_uuid.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_user_by_username(self, remnawave, test_user):
        user_username = await remnawave.users.get_user_by_username(
            username=test_user.username
        )
        assert isinstance(user_username, UserResponseDto)
        assert user_username.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_all_tags(self, remnawave):
        users_tags = await remnawave.users.get_all_tags()
        assert isinstance(users_tags, TagsResponseDto)

    @pytest.mark.asyncio
    async def test_get_user_accessible_nodes(self, remnawave, test_user):
        try:
            user_accessible_nodes = await remnawave.users.get_user_accessible_nodes(
                user_id=test_user.id
            )
            assert isinstance(user_accessible_nodes, GetUserAccessibleNodesResponseDto)
            assert isinstance(user_accessible_nodes.active_nodes, list)
        except ApiError as e:
            # This might fail if the user doesn't have access to any nodes
            # or if the feature is not available, which is acceptable for testing
            assert e.error.code in [
                ErrorCode.USER_NOT_FOUND,
            ]

    @pytest.mark.asyncio
    async def test_get_subscription_requests(self, remnawave, test_user):
        """Test fetching user subscription request history"""
        try:
            subscription_requests = (
                await remnawave.users.get_user_subscription_request_history(
                    user_id=test_user.id
                )
            )
            assert isinstance(
                subscription_requests, GetUserSubscriptionRequestHistoryResponseDto
            )
            assert hasattr(subscription_requests, "total")
            assert hasattr(subscription_requests, "records")
        except ApiError as e:
            # Этот блок должен срабатывать только если API вернуло ошибку
            # (404, 403 и т.д.), но не когда просто нет записей
            assert e.error.code in [ErrorCode.USER_NOT_FOUND]


class TestUserActions:
    """Тесты действий над пользователями"""

    @pytest.mark.asyncio
    async def test_reset_user_traffic(self, remnawave, test_user):
        user_reset_traffic = await remnawave.users.reset_user_traffic(
            user_id=test_user.id
        )
        assert isinstance(user_reset_traffic, UserResponseDto)
        assert user_reset_traffic.id == test_user.id
        assert user_reset_traffic.used_traffic_bytes == 0

    @pytest.mark.asyncio
    async def test_disable_enable_user(self, remnawave, test_user):
        # Disable user
        try:
            disable_user = await remnawave.users.disable_user(user_id=test_user.id)
            assert isinstance(disable_user, UserResponseDto)
            assert disable_user.id == test_user.id
            assert disable_user.status == UserStatus.DISABLED
        except ApiError as e:
            assert e.error.code == ErrorCode.USER_ALREADY_DISABLED

        # Enable user
        try:
            enable_user = await remnawave.users.enable_user(user_id=test_user.id)
            assert isinstance(enable_user, UserResponseDto)
            assert enable_user.id == test_user.id
            assert enable_user.status == UserStatus.ACTIVE
        except ApiError as e:
            assert e.error.code == ErrorCode.USER_ALREADY_ENABLED

    @pytest.mark.asyncio
    async def test_revoke_user_subscription(self, remnawave, test_user):
        old_short_uuid = test_user.short_uuid

        revoke_user_subscription = await remnawave.users.revoke_user_subscription(
            user_id=test_user.id
        )
        assert isinstance(revoke_user_subscription, UserResponseDto)
        assert revoke_user_subscription.id == test_user.id
        assert revoke_user_subscription.short_uuid != old_short_uuid


@pytest.fixture
async def test_user(remnawave):
    """Fixture to create a test user for tests"""
    username = generate_random_string(length=8)
    expire_at = datetime.now(tz=pytz.UTC) + timedelta(days=7)

    user = await remnawave.users.create_user(
        CreateUserRequestDto(
            username=username,
            expire_at=expire_at,
        )
    )

    yield user

    # Clean up
    await remnawave.users.delete_user(user_id=user.id)
