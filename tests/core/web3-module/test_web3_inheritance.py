from bubble import (
    BubbleTesterProvider,
    Web3,
)


def test_classes_may_inherit_from_web3():
    class InheritsFromWeb3(Web3):
        pass

    inherited_w3 = InheritsFromWeb3(BubbleTesterProvider())
    assert inherited_w3.bub.chain_id == 131277322940537
