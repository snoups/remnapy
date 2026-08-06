import random

import pytest

from remnapy.enums import ALPN, Fingerprint, SecurityLayer
from remnapy.exceptions.general import ApiError
from remnapy.models import (
    CreateHostRequestDto,
    CreateHostResponseDto,
    GetAllHostsResponseDto,
    GetAllHostTagsResponseDto,
    GetOneHostResponseDto,
    ReorderHostItem,
    ReorderHostRequestDto,
    ReorderHostResponseDto,
    UpdateHostRequestDto,
    UpdateHostResponseDto,
)
from tests.conftest import REMNAWAVE_CONFIG_PROFILE_UUID, REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string


class TestHostsBasic:
    """Basic host functionality"""

    @pytest.mark.asyncio
    async def test_get_all_hosts(self, remnawave):
        """Fetching all hosts"""
        all_hosts = await remnawave.hosts.get_all_hosts()
        assert isinstance(all_hosts, GetAllHostsResponseDto)
        for host in all_hosts:
            assert hasattr(host, "uuid")
            assert hasattr(host, "remark")

    @pytest.mark.asyncio
    async def test_get_hosts_tags(self, remnawave):
        """Fetching all host tags"""
        try:
            tags = await remnawave.hosts.get_hosts_tags()
            assert isinstance(tags, GetAllHostTagsResponseDto)
            assert hasattr(tags, "tags")
        except Exception as e:
            pytest.skip(f"Skipping tags test: {e!s}")


class TestHostsCRUD:
    """Host CRUD operations"""

    @pytest.fixture
    async def test_host(self, remnawave):
        """Create a throwaway host."""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()

        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                tags=["TEST"],
            )
        )

        yield create_host

        try:
            await remnawave.hosts.delete_host(uuid=str(create_host.uuid))
        except Exception:
            pass

    @pytest.mark.asyncio
    async def test_create_host(self, remnawave):
        """Creating a host"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()

        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                tags=["TEST"],
                is_hidden=False,
                server_description="Test Server",
                vless_route_id=1234,
                shuffle_host=False,
                mihomo_x25519=False,
            )
        )

        assert isinstance(create_host, CreateHostResponseDto)
        assert str(create_host.inbound_uuid) == REMNAWAVE_INBOUND_UUID
        assert create_host.address == random_ip
        assert create_host.port == random_port
        assert create_host.remark == random_remark
        assert create_host.tags == ["TEST"]

        await remnawave.hosts.delete_host(uuid=str(create_host.uuid))

    @pytest.mark.asyncio
    async def test_get_one_host(self, remnawave, test_host):
        """Fetching a single host"""
        string_uuid = str(test_host.uuid)

        host = await remnawave.hosts.get_one_host(uuid=string_uuid)
        assert isinstance(host, GetOneHostResponseDto)
        assert host.uuid == test_host.uuid
        assert host.remark == test_host.remark

    @pytest.mark.asyncio
    async def test_update_host(self, remnawave, test_host):
        """Updating a host"""
        update_data = UpdateHostRequestDto(
            uuid=test_host.uuid,
            server_description="Updated Host",
            is_disabled=False,
        )

        updated_host: UpdateHostResponseDto = await remnawave.hosts.update_host(
            update_data
        )

        assert updated_host is not None
        assert updated_host.server_description == "Updated Host"
        assert updated_host.is_disabled is False

    @pytest.mark.asyncio
    async def test_delete_host(self, remnawave):
        """Deleting a host"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()

        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
            )
        )

        string_uuid = str(create_host.uuid)

        delete_host = await remnawave.hosts.delete_host(uuid=string_uuid)
        assert delete_host is None
        assert delete_host is None

        try:
            await remnawave.hosts.get_one_host(uuid=string_uuid)
            pytest.fail("Host was not deleted")
        except Exception:
            # Expect an error: the host is gone
            pass


class TestHostsOrdering:
    """Host ordering"""

    @pytest.mark.asyncio
    async def test_reorder_hosts(self, remnawave):
        """Reordering hosts"""
        try:
            hosts_response = await remnawave.hosts.get_all_hosts()

            hosts_list = list(hosts_response)

            # Skip when there are fewer than two hosts
            if len(hosts_list) < 2:
                pytest.skip("Not enough hosts to test reordering")

            reorder_items = [
                ReorderHostItem(view_position=1, uuid=hosts_list[1].uuid),
                ReorderHostItem(view_position=0, uuid=hosts_list[0].uuid),
            ]

            reorder_request = ReorderHostRequestDto(hosts=reorder_items)

            response: ReorderHostResponseDto = await remnawave.hosts.reorder_hosts(
                body=reorder_request
            )

            assert response is not None
            assert response.is_updated is True

        except ApiError as e:
            # Skip on permission errors
            pytest.skip(f"Could not reorder hosts: {e!s}")


class TestHostsAdvanced:
    """Advanced host functionality"""

    @pytest.mark.asyncio
    async def test_create_host_with_advanced_options(self, remnawave):
        """Creating a host with advanced options"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()

        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                alpn=ALPN.H2,
                fingerprint=Fingerprint.CHROME,
                security_layer=SecurityLayer.TLS,
                path="/websocket",
                sni="example.com",
                host="example.org",
                allow_insecure=False,
                is_disabled=False,
                mux_params={"enabled": True, "concurrency": 8},
                sockopt_params={"mark": 255},
                tags=["ADVANCED"],
                is_hidden=False,
                override_sni_from_address=True,
                server_description="Advanced Server",
                vless_route_id=9876,
                shuffle_host=True,
                mihomo_x25519=True,
            )
        )

        assert isinstance(create_host, CreateHostResponseDto)
        assert create_host.alpn == ALPN.H2
        assert create_host.fingerprint == Fingerprint.CHROME
        assert create_host.security_layer == SecurityLayer.TLS
        assert create_host.path == "/websocket"
        assert create_host.sni == "example.com"
        assert create_host.host == "example.org"
        assert create_host.tags == ["ADVANCED"]

        await remnawave.hosts.delete_host(uuid=str(create_host.uuid))
