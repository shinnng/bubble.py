import pytest

from bubble.main import (
    Web3,
)
from bubble.providers.bub_tester import (
    BubbleTesterProvider,
)


@pytest.fixture(scope="module")
def w3():
    provider = BubbleTesterProvider()
    return Web3(provider)
