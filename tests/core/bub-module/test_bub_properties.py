import pytest

from bubble import (
    Web3,
)
from bubble.bub import (
    AsyncBub,
)
from bubble.providers.bub_tester.main import (
    AsyncBubereumTesterProvider,
)


@pytest.fixture
def async_w3():
    return Web3(
        AsyncBubereumTesterProvider(),
        middlewares=[],
        modules={
            "bub": (AsyncBub,),
        },
    )


def test_bub_chain_id(w3):
    assert w3.bub.chain_id == 131277322940537  # from fixture generation file


@pytest.mark.asyncio
async def test_async_bub_chain_id(async_w3):
    assert (
            await async_w3.bub.chain_id == 131277322940537
    )  # from fixture generation file
