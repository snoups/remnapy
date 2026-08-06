import pytest

from remnapy.exceptions import ApiError
from remnapy.models import (
    LoginRequestDto,
    LoginResponseDto,
)
from tests.conftest import REMNAWAVE_ADMIN_PASSWORD, REMNAWAVE_ADMIN_USERNAME


class TestAuthentication:
    """Authentication functionality"""

    @pytest.mark.asyncio
    async def test_login_with_credentials(self, remnawave):
        """Basic username/password authentication"""
        login = await remnawave.auth.login(
            LoginRequestDto(
                username=REMNAWAVE_ADMIN_USERNAME,
                password=REMNAWAVE_ADMIN_PASSWORD,
            )
        )
        assert isinstance(login, LoginResponseDto)
        assert login.access_token is not None
        # Check the token is present without touching the user field,
        # which this API version no longer returns
        assert login.access_token.startswith("eyJ")  # JWT tokens always start with eyJ

    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials(self, remnawave):
        """Authentication with invalid credentials"""
        try:
            await remnawave.auth.login(
                LoginRequestDto(
                    username="invalid_username",
                    password="invalid_password",
                )
            )
            pytest.fail("Expected authentication error for invalid credentials")
        except ApiError as e:
            assert e.status_code in [401, 403], (
                f"Expected 401 or 403, got {e.status_code}"
            )
