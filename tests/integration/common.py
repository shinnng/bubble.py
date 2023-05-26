import pytest

from websockets.exceptions import (
    ConnectionClosed,
)

from bubble import (
    Web3,
)

# use same coinbase value as in `bubble.py/tests/integration/generate_fixtures/common.py`
COINBASE = "0xdc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd"


class MiscWebsocketTest:
    def test_websocket_max_size_error(self, w3, endpoint_uri):
        w3 = Web3(
            Web3.WebsocketProvider(
                endpoint_uri=endpoint_uri, websocket_kwargs={"max_size": 1}
            )
        )
        with pytest.raises((OSError, ConnectionClosed)):
            w3.bub.get_block(0)
