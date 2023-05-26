from bubble import (
    Web3,
)
from bubble.providers.auto import (
    AutoProvider,
)
from bubble.providers.bub_tester import (
    BubbleTesterProvider,
)


def test_set_provider(w3):
    provider = BubbleTesterProvider()

    w3.provider = provider

    assert w3.provider == provider


def test_auto_provider_none():
    # init without provider succeeds, even when no provider available
    w3 = Web3()

    # non-node requests succeed
    w3.to_hex(0) == "0x0"

    type(w3.provider) == AutoProvider


def test_provider_default_value_for_ccip_read_redirect(w3):
    assert w3.provider.global_ccip_read_enabled
    assert w3.provider.ccip_read_max_redirects == 4
