from remnapy.models import GetNodeSecretKeyResponseDto
from remnapy.rapid import BaseController, get


class KeygenController(BaseController):
    @get("/keygen", response_class=GetNodeSecretKeyResponseDto)
    async def generate_key(
        self,
    ) -> GetNodeSecretKeyResponseDto:
        """Get SECRET_KEY for Remnawave Node"""
        ...
