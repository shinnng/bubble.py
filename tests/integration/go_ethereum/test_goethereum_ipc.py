import os
import pytest
import tempfile

from tests.integration.common import (
    COINBASE,
)
from tests.utils import (
    get_open_port,
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
from .utils import (
    wait_for_socket,
)


def _bub_command_arguments(bub_ipc_path, base_bub_command_arguments):
    bub_port = get_open_port()
    yield from base_bub_command_arguments
    yield from (
        "--port",
        bub_port,
        "--ipcpath",
        bub_ipc_path,
        "--miner.etherbase",
        COINBASE[2:],
        "--rpc.enabledeprecatedpersonal",
    )


@pytest.fixture(scope="module")
def bub_command_arguments(bub_ipc_path, base_bub_command_arguments):
    return _bub_command_arguments(bub_ipc_path, base_bub_command_arguments)


@pytest.fixture(scope="module")
def bub_ipc_path(datadir):
    bub_ipc_dir_path = tempfile.mkdtemp()
    _bub_ipc_path = os.path.join(bub_ipc_dir_path, "bub.ipc")
    yield _bub_ipc_path

    if os.path.exists(_bub_ipc_path):
        os.remove(_bub_ipc_path)


@pytest.fixture(scope="module")
def w3(bub_process, bub_ipc_path):
    wait_for_socket(bub_ipc_path)
    _w3 = Web3(Web3.IPCProvider(bub_ipc_path, timeout=30))
    return _w3


class TestGoEthereumTest(GoEthereumTest):
    pass


class TestGoEthereumAdminModuleTest(GoEthereumAdminModuleTest):
    @pytest.mark.xfail(
        reason="running bub with the --nodiscover flag doesn't allow peer addition"
    )
    def test_admin_peers(w3):
        super().test_admin_peers(w3)

    def test_admin_start_stop_http(self, w3: "Web3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(
            reason="Only one HTTP endpoint is allowed to be active at any time"
        )
        super().test_admin_start_stop_http(w3)

    def test_admin_start_stop_ws(self, w3: "Web3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(reason="Only one WS endpoint is allowed to be active at any time")
        super().test_admin_start_stop_ws(w3)


class TestGoEthereumEthModuleTest(GoEthereumEthModuleTest):
    pass


class TestGoEthereumNetModuleTest(GoEthereumNetModuleTest):
    pass


class TestGoEthereumPersonalModuleTest(GoEthereumPersonalModuleTest):
    pass
