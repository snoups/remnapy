from pydantic import BaseModel, Field


class GetNodeSecretKeyResponseDto(BaseModel):
    """Response for GET /api/keygen: SECRET_KEY for a Remnawave node"""

    secret_key: str = Field(alias="secretKey")
