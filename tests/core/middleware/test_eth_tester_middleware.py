import pytest
from unittest.mock import (
    Mock,
)

from bubble.providers.bub_tester.middleware import (
    async_default_transaction_fields_middleware,
    default_transaction_fields_middleware,
)
from bubble.types import (
    BlockData,
)

SAMPLE_ADDRESS_LIST = [
    "0x0000000000000000000000000000000000000001",
    "0x0000000000000000000000000000000000000002",
    "0x0000000000000000000000000000000000000003",
]
SAMPLE_ADDRESS = "0x0000000000000000000000000000000000000004"


@pytest.mark.parametrize("block_number", {0, "0x0", "earliest"})
def test_get_transaction_count_formatters(w3, block_number):
    tx_counts = w3.bub.get_transaction_count(w3.bub.accounts[-1], block_number)
    assert tx_counts == 0


def test_get_block_formatters(w3):
    all_block_keys = BlockData.__annotations__.keys()
    all_non_poa_block_keys = set(
        [k for k in all_block_keys if k != "proofOfAuthorityData"]
    )

    latest_block = w3.bub.get_block("latest")
    latest_block_keys = set(latest_block.keys())
    assert all_non_poa_block_keys == latest_block_keys


@pytest.mark.parametrize(
    "w3_accounts, w3_coinbase, method, from_field_added, from_field_value",
    (
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_call", True, SAMPLE_ADDRESS),
        (
            SAMPLE_ADDRESS_LIST,
            SAMPLE_ADDRESS,
            "bub_estimateGas",
            True,
            SAMPLE_ADDRESS,
        ),
        (
            SAMPLE_ADDRESS_LIST,
            SAMPLE_ADDRESS,
            "bub_sendTransaction",
            True,
            SAMPLE_ADDRESS,
        ),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_gasPrice", False, None),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_blockNumber", False, None),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "meow", False, None),
        (SAMPLE_ADDRESS_LIST, None, "bub_call", True, SAMPLE_ADDRESS_LIST[0]),
        (SAMPLE_ADDRESS_LIST, None, "bub_estimateGas", True, SAMPLE_ADDRESS_LIST[0]),
        (
            SAMPLE_ADDRESS_LIST,
            None,
            "bub_sendTransaction",
            True,
            SAMPLE_ADDRESS_LIST[0],
        ),
        (SAMPLE_ADDRESS_LIST, None, "bub_gasPrice", False, None),
        (SAMPLE_ADDRESS_LIST, None, "bub_blockNumber", False, None),
        (SAMPLE_ADDRESS_LIST, None, "meow", False, None),
        (None, SAMPLE_ADDRESS, "bub_call", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_estimateGas", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_sendTransaction", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_gasPrice", False, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_blockNumber", False, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "meow", False, SAMPLE_ADDRESS),
        (None, None, "bub_call", True, None),
        (None, None, "bub_estimateGas", True, None),
        (None, None, "bub_sendTransaction", True, None),
        (None, None, "bub_gasPrice", False, None),
        (None, None, "bub_blockNumber", False, None),
        (None, None, "meow", False, None),
    ),
)
def test_default_transaction_fields_middleware(
    w3_accounts, w3_coinbase, method, from_field_added, from_field_value
):
    def mock_request(_method, params):
        return params

    mock_w3 = Mock()
    mock_w3.bub.accounts = w3_accounts
    mock_w3.bub.coinbase = w3_coinbase

    middleware = default_transaction_fields_middleware(mock_request, mock_w3)
    base_params = {"chainId": 5}
    filled_transaction = middleware(method, [base_params])

    filled_params = filled_transaction[0]

    assert ("from" in filled_params.keys()) == from_field_added
    if "from" in filled_params.keys():
        assert filled_params["from"] == from_field_value

    filled_transaction[0].pop("from", None)
    assert filled_transaction[0] == base_params


# -- async -- #


@pytest.mark.parametrize(
    "w3_accounts, w3_coinbase, method, from_field_added, from_field_value",
    (
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_call", True, SAMPLE_ADDRESS),
        (
            SAMPLE_ADDRESS_LIST,
            SAMPLE_ADDRESS,
            "bub_estimateGas",
            True,
            SAMPLE_ADDRESS,
        ),
        (
            SAMPLE_ADDRESS_LIST,
            SAMPLE_ADDRESS,
            "bub_sendTransaction",
            True,
            SAMPLE_ADDRESS,
        ),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_gasPrice", False, None),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "bub_blockNumber", False, None),
        (SAMPLE_ADDRESS_LIST, SAMPLE_ADDRESS, "meow", False, None),
        (SAMPLE_ADDRESS_LIST, None, "bub_call", True, SAMPLE_ADDRESS_LIST[0]),
        (SAMPLE_ADDRESS_LIST, None, "bub_estimateGas", True, SAMPLE_ADDRESS_LIST[0]),
        (
            SAMPLE_ADDRESS_LIST,
            None,
            "bub_sendTransaction",
            True,
            SAMPLE_ADDRESS_LIST[0],
        ),
        (SAMPLE_ADDRESS_LIST, None, "bub_gasPrice", False, None),
        (SAMPLE_ADDRESS_LIST, None, "bub_blockNumber", False, None),
        (SAMPLE_ADDRESS_LIST, None, "meow", False, None),
        (None, SAMPLE_ADDRESS, "bub_call", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_estimateGas", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_sendTransaction", True, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_gasPrice", False, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "bub_blockNumber", False, SAMPLE_ADDRESS),
        (None, SAMPLE_ADDRESS, "meow", False, SAMPLE_ADDRESS),
        (None, None, "bub_call", True, None),
        (None, None, "bub_estimateGas", True, None),
        (None, None, "bub_sendTransaction", True, None),
        (None, None, "bub_gasPrice", False, None),
        (None, None, "bub_blockNumber", False, None),
        (None, None, "meow", False, None),
    ),
)
@pytest.mark.asyncio
async def test_async_default_transaction_fields_middleware(
    w3_accounts,
    w3_coinbase,
    method,
    from_field_added,
    from_field_value,
):
    async def mock_request(_method, params):
        return params

    async def mock_async_accounts():
        return w3_accounts

    async def mock_async_coinbase():
        return w3_coinbase

    mock_w3 = Mock()
    mock_w3.bub.accounts = mock_async_accounts()
    mock_w3.bub.coinbase = mock_async_coinbase()

    middleware = await async_default_transaction_fields_middleware(
        mock_request, mock_w3
    )
    base_params = {"chainId": 5}
    filled_transaction = await middleware(method, [base_params])

    filled_params = filled_transaction[0]
    assert ("from" in filled_params.keys()) == from_field_added
    if "from" in filled_params.keys():
        assert filled_params["from"] == from_field_value

    filled_transaction[0].pop("from", None)
    assert filled_transaction[0] == base_params

    # clean up
    mock_w3.bub.accounts.close()
    mock_w3.bub.coinbase.close()
