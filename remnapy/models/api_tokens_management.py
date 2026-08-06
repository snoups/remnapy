from datetime import datetime

from pydantic import BaseModel, Field


class CreateApiTokenRequestDto(BaseModel):
    name: str
    expires_in_days: int = Field(serialization_alias="expiresInDays")
    scopes: list[str] = Field(default_factory=lambda: ["*"])


class ApiTokenDto(BaseModel):
    uuid: str
    name: str
    expire_at: datetime = Field(..., alias="expireAt")
    scopes: list[str]
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class CreateApiTokenResponseDto(ApiTokenDto):
    token: str


class FindAllApiTokensResponseData(BaseModel):
    tokens: list[ApiTokenDto]


class FindAllApiTokensResponseDto(FindAllApiTokensResponseData):
    pass


class ApiTokenScopeEndpointDto(BaseModel):
    key: str
    kind: str
    method: str
    path: str
    description: str


class ApiTokenScopeResourceDto(BaseModel):
    resource: str
    resource_scopes: list[str] = Field(..., alias="resourceScopes")
    endpoints: list[ApiTokenScopeEndpointDto]


class GetApiTokenScopesResponseData(BaseModel):
    wildcard: str
    resources: list[ApiTokenScopeResourceDto]


class GetApiTokenScopesResponseDto(GetApiTokenScopesResponseData):
    pass
