import random

from flaky import (
    flaky,
)

from bubble._utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_stop(w3_empty):
    w3 = w3_empty

    assert w3.bub.mining
    assert w3.bub.hashrate

    w3.bub.miner.stop()

    with Timeout(60) as timeout:
        while w3.bub.mining or w3.bub.hashrate:
            timeout.sleep(random.random())
            timeout.check()

    assert not w3.bub.mining
    assert not w3.bub.hashrate
