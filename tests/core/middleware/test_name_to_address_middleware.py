import pytest

from bubble import (
    Web3,
    constants,
)
from bubble.exceptions import (
    InvalidAddress,
)
from bubble.middleware import (  # noqa: F401
    construct_fixture_middleware,
    name_to_address_middleware,
)
from bubble.providers.base import (
    BaseProvider,
)

NAME = "dump.bub"
ADDRESS = constants.ADDRESS_ZERO
BALANCE = 0


class TempENS:
    def __init__(self, name_addr_pairs):
        self.registry = dict(name_addr_pairs)

    def address(self, name):
        return self.registry.get(name, None)


@pytest.fixture
def w3():
    w3 = Web3(provider=BaseProvider(), middlewares=[])
    w3.ens = TempENS({NAME: ADDRESS})
    w3.middleware_onion.add(name_to_address_middleware(w3))
    return w3


def test_pass_name_resolver(w3):
    return_chain_on_mainnet = construct_fixture_middleware(
        {
            "net_version": "1",
        }
    )
    return_balance = construct_fixture_middleware({"bub_getBalance": BALANCE})
    w3.middleware_onion.inject(return_chain_on_mainnet, layer=0)
    w3.middleware_onion.inject(return_balance, layer=0)
    assert w3.bub.get_balance(NAME) == BALANCE


def test_fail_name_resolver(w3):
    return_chain_on_mainnet = construct_fixture_middleware(
        {
            "net_version": "2",
        }
    )
    w3.middleware_onion.inject(return_chain_on_mainnet, layer=0)
    with pytest.raises(InvalidAddress, match=r".*ethereum\.bub.*"):
        w3.bub.get_balance("ethereum.bub")
