import pytest

import pytest_asyncio

from bubble import (
    Web3,
)
from bubble._utils.filters import (
    AsyncBlockFilter,
    AsyncLogFilter,
    AsyncTransactionFilter,
    BlockFilter,
    LogFilter,
    TransactionFilter,
)
from bubble.bub import (
    AsyncBub,
)
from bubble.providers.bub_tester.main import (
    AsyncBubereumTesterProvider,
)


def test_bub_filter_creates_correct_filter_type(w3):
    filter1 = w3.bub.filter("latest")
    assert isinstance(filter1, BlockFilter)
    filter2 = w3.bub.filter("pending")
    assert isinstance(filter2, TransactionFilter)
    filter3 = w3.bub.filter({})
    assert isinstance(filter3, LogFilter)


# --- async --- #


@pytest_asyncio.fixture()
async def async_w3():
    provider = AsyncBubereumTesterProvider()
    w3 = Web3(provider, modules={"bub": [AsyncBub]}, middlewares=[])
    return w3


@pytest.mark.asyncio
async def test_AsyncBub_filter_creates_correct_filter_type(async_w3):
    filter1 = await async_w3.bub.filter("latest")
    assert isinstance(filter1, AsyncBlockFilter)
    filter2 = await async_w3.bub.filter("pending")
    assert isinstance(filter2, AsyncTransactionFilter)
    filter3 = await async_w3.bub.filter({})
    assert isinstance(filter3, AsyncLogFilter)
