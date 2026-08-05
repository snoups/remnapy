from pydantic import BaseModel, Field


class PubKeyData(BaseModel):
    pub_key: str = Field(alias="pubKey")


class GetPubKeyResponseDto(BaseModel):
    secret_key: str = Field(alias="secretKey")


# Legacy alias for backward compatibility
PubKeyResponseDto = PubKeyData
