import pytest

from remnapy.models import GetNodeSecretKeyResponseDto


@pytest.mark.asyncio
async def test_keygen(remnawave):
    key = await remnawave.keygen.generate_key()
    assert isinstance(key, GetNodeSecretKeyResponseDto)
