"""Metadata management models for Users and Nodes"""

from typing import Any, Optional

from pydantic import BaseModel


class GetMetadataResponseDto(BaseModel):
    """Get metadata response"""

    metadata: Optional[dict[str, Any]] = None


class GetUserMetadataResponseDto(BaseModel):
    """Get user metadata response"""

    metadata: Optional[dict[str, Any]] = None


class UpsertUserMetadataRequestBodyDto(BaseModel):
    """Request body for upserting user metadata"""

    metadata: dict[str, Any]


class UpsertUserMetadataResponseDto(BaseModel):
    """Response for upserting user metadata"""

    metadata: dict[str, Any]


class GetNodeMetadataResponseDto(BaseModel):
    """Get node metadata response"""

    metadata: Optional[dict[str, Any]] = None


class UpsertNodeMetadataRequestBodyDto(BaseModel):
    """Request body for upserting node metadata"""

    metadata: dict[str, Any]


class UpsertNodeMetadataResponseDto(BaseModel):
    """Response for upserting node metadata"""

    metadata: dict[str, Any]
