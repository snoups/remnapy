from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class InboundResponseDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")
    active_squads: list[UUID] = Field(default_factory=list, alias="activeSquads")


class AllInboundsData(BaseModel):
    total: float
    inbounds: list[InboundResponseDto]


class GetAllInboundsResponseDto(AllInboundsData):
    pass


class InboundsByProfileData(BaseModel):
    total: float
    inbounds: list[InboundResponseDto]


class GetInboundsByProfileUuidResponseDto(InboundsByProfileData):
    pass


# Legacy models for backward compatibility
class GetInboundsResponseDto(RootModel[list[InboundResponseDto]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


class FullInboundStatistic(BaseModel):
    enabled: float
    disabled: float


class FullInboundResponseDto(BaseModel):
    uuid: UUID
    tag: str
    type: str
    port: float
    network: Optional[str] = None
    security: Optional[str] = None
    raw_from_config: Any = Field(alias="rawFromConfig")
    users: FullInboundStatistic
    nodes: FullInboundStatistic


class GetFullInboundsResponseDto(RootModel[list[FullInboundResponseDto]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)

    def __len__(self):
        """Return length of list"""
        return len(self.root)


# Legacy aliases for backward compatibility
InboundsResponseDto = GetInboundsResponseDto
FullInboundsResponseDto = GetFullInboundsResponseDto
