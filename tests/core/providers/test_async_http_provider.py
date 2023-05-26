import pytest

from aiohttp import (
    ClientSession,
)

from bubble import (
    AsyncWeb3,
)
from bubble._utils import (
    request,
)
from bubble.bub import (
    AsyncBub,
)
from bubble.exceptions import (
    ProviderConnectionError,
)
from bubble.node import (
    AsyncNode,
    AsyncNodeAdmin,
    AsyncNodePersonal,
    AsyncNodeTxPool,
)
from bubble.middleware import (
    async_attrdict_middleware,
    async_buffered_gas_estimate_middleware,
    async_gas_price_strategy_middleware,
    async_validation_middleware,
)
from bubble.net import (
    AsyncNet,
)
from bubble.providers.async_rpc import (
    AsyncHTTPProvider,
)

URI = "http://mynode.local:8545"


async def clean_async_session_cache():
    cache_data = request._async_session_cache._data
    while len(cache_data) > 0:
        _key, cached_session = cache_data.popitem()
        await cached_session.close()


@pytest.mark.asyncio
async def test_no_args() -> None:
    provider = AsyncHTTPProvider()
    w3 = AsyncWeb3(provider)
    assert w3.manager.provider == provider
    assert w3.manager.provider.is_async
    assert not await w3.is_connected()
    with pytest.raises(ProviderConnectionError):
        await w3.is_connected(show_traceback=True)

    await clean_async_session_cache()
    assert len(request._async_session_cache) == 0


def test_init_kwargs():
    provider = AsyncHTTPProvider(endpoint_uri=URI, request_kwargs={"timeout": 60})
    w3 = AsyncWeb3(provider)
    assert w3.manager.provider == provider


def test_web3_with_async_http_provider_has_default_middlewares_and_modules() -> None:
    async_w3 = AsyncWeb3(AsyncHTTPProvider(endpoint_uri=URI))

    # assert default modules

    assert isinstance(async_w3.bub, AsyncBub)
    assert isinstance(async_w3.net, AsyncNet)
    assert isinstance(async_w3.node, AsyncNode)
    assert isinstance(async_w3.node.admin, AsyncNodeAdmin)
    assert isinstance(async_w3.node.personal, AsyncNodePersonal)
    assert isinstance(async_w3.node.txpool, AsyncNodeTxPool)

    # assert default middleware

    # the following length check should fail and will need to be added to once more
    # async middlewares are added to the defaults
    assert len(async_w3.middleware_onion.middlewares) == 4

    assert (
        async_w3.middleware_onion.get("gas_price_strategy")
        == async_gas_price_strategy_middleware
    )
    assert async_w3.middleware_onion.get("attrdict") == async_attrdict_middleware
    assert async_w3.middleware_onion.get("validation") == async_validation_middleware
    assert (
        async_w3.middleware_onion.get("gas_estimate")
        == async_buffered_gas_estimate_middleware
    )


@pytest.mark.asyncio
async def test_user_provided_session() -> None:
    session = ClientSession()
    provider = AsyncHTTPProvider(endpoint_uri=URI)
    cached_session = await provider.cache_async_session(session)
    assert len(request._async_session_cache) == 1
    assert cached_session == session
