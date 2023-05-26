import random

from flaky import (
    flaky,
)

from bubble._utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_set_gas_price(web3_empty, wait_for_block):
    web3 = web3_empty

    initial_gas_price = web3.bub.gas_price

    # sanity check
    assert web3.bub.gas_price > 1000

    web3.bub.miner.set_gas_price(initial_gas_price // 2)

    with Timeout(60) as timeout:
        while web3.bub.gas_price == initial_gas_price:
            timeout.sleep(random.random())

    after_gas_price = web3.bub.gas_price
    assert after_gas_price < initial_gas_price
