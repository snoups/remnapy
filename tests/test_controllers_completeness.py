"""Tests that all required endpoints exist in controllers."""

from remnapy.controllers.connections import ConnectionsController
from remnapy.controllers.system import SystemController
from remnapy.controllers.users import UsersController


class TestUsersControllerEndpoints:
    def test_has_resolve_user(self):
        assert hasattr(UsersController, "resolve_user")
        assert callable(UsersController.resolve_user)

    def test_has_revoke_user_subscription(self):
        assert hasattr(UsersController, "revoke_user_subscription")

    def test_has_disable_user(self):
        assert hasattr(UsersController, "disable_user")

    def test_has_enable_user(self):
        assert hasattr(UsersController, "enable_user")

    def test_has_reset_user_traffic(self):
        assert hasattr(UsersController, "reset_user_traffic")

    def test_has_create_user(self):
        assert hasattr(UsersController, "create_user")

    def test_has_update_user(self):
        assert hasattr(UsersController, "update_user")

    def test_has_delete_user(self):
        assert hasattr(UsersController, "delete_user")

    def test_has_get_all_users(self):
        assert hasattr(UsersController, "get_all_users")

    def test_has_get_user_by_id(self):
        assert hasattr(UsersController, "get_user_by_id")

    def test_has_get_user_by_short_uuid(self):
        assert hasattr(UsersController, "get_user_by_short_uuid")

    def test_has_get_user_by_username(self):
        assert hasattr(UsersController, "get_user_by_username")

    def test_has_get_all_tags(self):
        assert hasattr(UsersController, "get_all_tags")

    def test_has_get_user_accessible_nodes(self):
        assert hasattr(UsersController, "get_user_accessible_nodes")

    def test_has_get_user_subscription_request_history(self):
        assert hasattr(UsersController, "get_user_subscription_request_history")

    def test_has_extend_user(self):
        assert hasattr(UsersController, "extend_user")


class TestSystemControllerEndpoints:
    def test_has_get_recap(self):
        assert hasattr(SystemController, "get_recap")
        assert callable(SystemController.get_recap)

    def test_has_get_metadata(self):
        assert hasattr(SystemController, "get_metadata")

    def test_has_get_stats(self):
        assert hasattr(SystemController, "get_stats")

    def test_has_get_bandwidth_stats(self):
        assert hasattr(SystemController, "get_bandwidth_stats")

    def test_has_get_nodes_statistics(self):
        assert hasattr(SystemController, "get_nodes_statistics")

    def test_has_get_health(self):
        assert hasattr(SystemController, "get_health")

    def test_has_get_nodes_metrics(self):
        assert hasattr(SystemController, "get_nodes_metrics")

    def test_has_get_x25519_key_pair(self):
        assert hasattr(SystemController, "get_x25519_key_pair")

    def test_has_debug_srr_matcher(self):
        assert hasattr(SystemController, "debug_srr_matcher")

    def test_has_get_configuration(self):
        assert hasattr(SystemController, "get_configuration")

    def test_has_get_stats_digest(self):
        assert hasattr(SystemController, "get_stats_digest")

    def test_has_get_http_stats(self):
        assert hasattr(SystemController, "get_http_stats")


class TestConnectionsControllerEndpoints:
    def test_has_connections_by_node(self):
        assert hasattr(ConnectionsController, "connections_by_node")

    def test_has_connections_by_node_result(self):
        assert hasattr(ConnectionsController, "connections_by_node_result")

    def test_has_connections_by_user(self):
        assert hasattr(ConnectionsController, "connections_by_user")

    def test_has_connections_by_user_result(self):
        assert hasattr(ConnectionsController, "connections_by_user_result")

    def test_has_drop_connections(self):
        assert hasattr(ConnectionsController, "drop_connections")
