import pytest

import pytest_asyncio

from bubble import (
    Web3,
)
from bubble.bub import (
    AsyncBub,
)
from bubble.module import (
    Module,
)
from bubble.providers.bub_tester.main import (
    AsyncBubereumTesterProvider,
)

# --- inherit from `bubble.module.Module` class --- #


@pytest.fixture(scope="module")
def module1():
    class Module1(Module):
        a = "a"

        @property
        def b(self):
            return "b"

    return Module1


@pytest.fixture(scope="module")
def module2():
    class Module2(Module):
        c = "c"

        @staticmethod
        def d():
            return "d"

    return Module2


@pytest.fixture(scope="module")
def module3():
    class Module3(Module):
        e = "e"

    return Module3


@pytest.fixture(scope="module")
def module4():
    class Module4(Module):
        f = "f"

    return Module4


# --- do not inherit from `bubble.module.Module` class --- #


@pytest.fixture(scope="module")
def module1_unique():
    # uses ``Web3`` instance by accepting it as first arg in the ``__init__()`` method
    class Module1:
        a = "a"

        def __init__(self, w3):
            self._b = "b"
            self.w3 = w3

        def b(self):
            return self._b

        @property
        def return_bub_chain_id(self):
            return self.w3.bub.chain_id

    return Module1


@pytest.fixture(scope="module")
def module2_unique():
    class Module2:
        c = "c"

        @staticmethod
        def d():
            return "d"

    return Module2


@pytest.fixture(scope="module")
def module3_unique():
    class Module3:
        e = "e"

    return Module3


@pytest.fixture(scope="module")
def module4_unique():
    class Module4:
        f = "f"

    return Module4


@pytest.fixture(scope="module")
def module_many_init_args():
    class ModuleManyArgs:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    return ModuleManyArgs


@pytest_asyncio.fixture()
async def async_w3():
    provider = AsyncBubereumTesterProvider()
    w3 = Web3(provider, modules={"bub": [AsyncBub]}, middlewares=provider.middlewares)
    w3.bub.default_account = await w3.bub.coinbase
    return w3


@pytest_asyncio.fixture()
async def async_w3_non_strict_abi():
    provider = AsyncBubereumTesterProvider()
    w3 = Web3(provider, modules={"bub": [AsyncBub]}, middlewares=provider.middlewares)
    w3.strict_bytes_type_checking = False
    w3.bub.default_account = await w3.bub.coinbase
    return w3
