import asyncio
import pytest

from tests.integration.common import (
    COINBASE,
    MiscWebsocketTest,
)
from tests.utils import (
    get_open_port,
    wait_for_ws,
)
from bubble import (
    Web3,
)

from .common import (
    GoEthereumAdminModuleTest,
    GoEthereumEthModuleTest,
    GoEthereumNetModuleTest,
    GoEthereumPersonalModuleTest,
    GoEthereumTest,
)


@pytest.fixture(scope="module")
def ws_port():
    return get_open_port()


@pytest.fixture(scope="module")
def endpoint_uri(ws_port):
    return f"ws://localhost:{ws_port}"


def _bub_command_arguments(ws_port, base_bub_command_arguments, bub_version):
    yield from base_bub_command_arguments
    if bub_version.major == 1:
        yield from (
            "--miner.etherbase",
            COINBASE[2:],
            "--ws",
            "--ws.port",
            ws_port,
            "--ws.api",
            "admin,bub,net,bubble,personal,miner",
            "--ws.origins",
            "*",
            "--ipcdisable",
            "--allow-insecure-unlock",
        )
        if bub_version.minor not in [10, 11]:
            raise AssertionError("Unsupported Bub version")
    else:
        raise AssertionError("Unsupported Bub version")


@pytest.fixture(scope="module")
def bub_command_arguments(
    bub_binary, get_bub_version, datadir, ws_port, base_bub_command_arguments
):
    return _bub_command_arguments(
        ws_port, base_bub_command_arguments, get_bub_version
    )


@pytest.fixture(scope="module")
def w3(bub_process, endpoint_uri):
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(wait_for_ws(endpoint_uri))
    _w3 = Web3(Web3.WebsocketProvider(endpoint_uri, websocket_timeout=30))
    return _w3


class TestGoEthereumTest(GoEthereumTest):
    pass


class TestGoEthereumAdminModuleTest(GoEthereumAdminModuleTest):
    @pytest.mark.xfail(
        reason="running bub with the --nodiscover flag doesn't allow peer addition"
    )
    def test_admin_peers(self, w3: "Web3") -> None:
        super().test_admin_peers(w3)

    def test_admin_start_stop_http(self, w3: "Web3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(
            reason="Only one HTTP endpoint is allowed to be active at any time"
        )
        super().test_admin_start_stop_http(w3)

    def test_admin_start_stop_ws(self, w3: "Web3") -> None:
        # This test inconsistently causes all tests after it to
        # fail on CI if it's allowed to run
        pytest.xfail(
            reason="Only one WebSocket endpoint is allowed to be active at any time"
        )
        super().test_admin_start_stop_ws(w3)


class TestGoEthereumEthModuleTest(GoEthereumEthModuleTest):
    pass


class TestGoEthereumNetModuleTest(GoEthereumNetModuleTest):
    pass


class TestGoEthereumPersonalModuleTest(GoEthereumPersonalModuleTest):
    pass


class TestMiscWebsocketTest(MiscWebsocketTest):
    pass
