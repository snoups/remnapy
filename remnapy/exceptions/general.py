from datetime import datetime
from typing import Any, Optional

from pydantic import AliasChoices, BaseModel, Field

from remnapy.enums import ErrorCode


class ApiErrorResponse(BaseModel):
    """Standard API error response model"""

    timestamp: Optional[datetime] = Field(
        None, description="When the error occurred"
    )
    path: Optional[str] = Field(None, description="Request path")
    message: str = Field(..., description="Error message")
    code: Optional[ErrorCode | str] = Field(
        None,
        validation_alias=AliasChoices("errorCode", "code", "error_code"),
        description="Error code",
    )
    # Support for API v2 error format
    status_code: Optional[int] = Field(None, alias="statusCode")
    errors: Optional[list[Any]] = Field(None, description="Validation error details")


class ApiError(Exception):
    """Base API error exception"""

    def __init__(self, status_code: int, error: ApiErrorResponse):
        self.status_code = status_code
        self.error = error
        super().__init__(
            f"API Error {error.code}: {error.message} (HTTP {status_code})"
        )

    @property
    def code(self) -> Optional[str]:
        """Get error code"""
        return self.error.code

    @property
    def message(self) -> str:
        """Get error message"""
        return self.error.message

    @property
    def timestamp(self) -> Optional[datetime]:
        """Get error timestamp"""
        return self.error.timestamp

    @property
    def path(self) -> Optional[str]:
        """Get request path"""
        return self.error.path


class BadRequestError(ApiError):
    """Client error (400)"""

    pass


class UnauthorizedError(ApiError):
    """Authentication required (401)"""

    pass


class ForbiddenError(ApiError):
    """Access forbidden (403)"""

    pass


class NotFoundError(ApiError):
    """Resource not found (404)"""

    pass


class ConflictError(ApiError):
    """Conflict (409)"""

    pass


class ValidationError(ApiError):
    """Validation error (422)"""

    pass


class ServerError(ApiError):
    """Server error (500+)"""

    pass


class NetworkError(ApiError):
    """Network-level failure"""

    pass


class AuthenticationError(ApiError):
    """Authentication failure"""

    pass


class BusinessLogicError(ApiError):
    """Business-logic failure"""

    pass


class RateLimitError(BadRequestError):
    """Request rate limit exceeded"""

    pass


class MaintenanceError(ServerError):
    """Panel is in maintenance mode"""

    pass


class QuotaExceededError(BusinessLogicError):
    """Quota exceeded"""

    pass


class FeatureNotAvailableError(BusinessLogicError):
    """Feature not available"""

    pass
