import pytest

from eth_tester.exceptions import (
    TransactionFailed,
)

from bubble.providers.bub_tester.main import (
    AsyncBubereumTesterProvider,
)
from bubble.types import (
    RPCEndpoint,
)


@pytest.mark.asyncio
async def test_async_tester_provider_is_connected() -> None:
    provider = AsyncBubereumTesterProvider()
    connected = await provider.is_connected()
    assert connected


@pytest.mark.asyncio
async def test_async_tester_provider_creates_a_block() -> None:
    provider = AsyncBubereumTesterProvider()
    accounts = await provider.make_request("bub_accounts", [])
    a, b = accounts["result"][:2]
    current_block = await provider.make_request("bub_blockNumber", [])
    assert current_block["result"] == 0
    tx = await provider.make_request(
        "bub_sendTransaction", [{"from": a, "to": b, "gas": 21000}]
    )
    assert tx
    current_block = await provider.make_request("bub_blockNumber", [])
    assert current_block["result"] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception_case",
    (
        # exception with bytes-encoded reason:
        TransactionFailed(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12The error message.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # noqa: E501
        ),
        # wrapped exceptions with bytes-encoded reason:
        TransactionFailed(
            Exception(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12The error message.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # noqa: E501
            )
        ),
        TransactionFailed("The error message."),
        TransactionFailed(Exception("The error message.")),
    ),
)
async def test_async_tester_provider_properly_handles_bub_tester_error_messages(
    mocker,
    exception_case,
):
    mocker.patch(
        "bub_tester.main.EthereumTester.get_block_by_number", side_effect=exception_case
    )

    provider = AsyncBubereumTesterProvider()
    with pytest.raises(
        TransactionFailed, match="execution reverted: The error message."
    ):
        await provider.make_request(RPCEndpoint("bub_blockNumber"), [])
