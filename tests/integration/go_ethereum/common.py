import pytest
from typing import (
    TYPE_CHECKING,
)

from eth_typing import (
    ChecksumAddress,
)

from bubble._utils.module_testing import (  # noqa: F401
    AsyncBubModuleTest,
    AsyncNetModuleTest,
    EthModuleTest,
    GoEthereumAdminModuleTest,
    GoEthereumAsyncTxPoolModuleTest,
    GoEthereumPersonalModuleTest,
    GoEthereumTxPoolModuleTest,
    NetModuleTest,
    Web3ModuleTest,
)
from bubble.types import (
    BlockData,
)

if TYPE_CHECKING:
    from bubble import (  # noqa: F401
        Web3,
    )


class GoEthereumTest(Web3ModuleTest):
    def _check_web3_client_version(self, client_version):
        assert client_version.startswith("Bub/")


class GoEthereumEthModuleTest(EthModuleTest):
    @pytest.mark.xfail(reason="bub_signTypedData has not been released in bub")
    def test_bub_sign_typed_data(self, w3, unlocked_account_dual_type):
        super().test_bub_sign_typed_data(w3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason="bub_signTypedData has not been released in bub")
    def test_invalid_bub_sign_typed_data(self, w3, unlocked_account_dual_type):
        super().test_invalid_bub_sign_typed_data(w3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason="Inconsistently creating timeout issues.", strict=False)
    def test_bub_estimate_gas(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        super().test_bub_estimate_gas(w3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason="Inconsistently creating timeout issues.", strict=False)
    def test_bub_estimate_gas_with_block(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        super().test_bub_estimate_gas_with_block(w3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason="Inconsistently creating timeout issues.", strict=False)
    def test_bub_get_transaction_receipt_unmined(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        super().test_bub_get_transaction_receipt_unmined(w3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason="Inconsistently creating timeout issues.", strict=False)
    def test_bub_wait_for_transaction_receipt_unmined(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        super().test_bub_wait_for_transaction_receipt_unmined(
            w3, unlocked_account_dual_type
        )

    @pytest.mark.xfail(reason="Inconsistently creating timeout issues.", strict=False)
    def test_bub_get_raw_transaction_by_block(
        self,
        w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
        block_with_txn: BlockData,
    ) -> None:
        super().test_bub_get_raw_transaction_by_block(
            w3, unlocked_account_dual_type, block_with_txn
        )


class GoEthereumNetModuleTest(NetModuleTest):
    pass


class GoEthereumAsyncNetModuleTest(AsyncNetModuleTest):
    pass


class GoEthereumAdminModuleTest(GoEthereumAdminModuleTest):
    pass


class GoEthereumPersonalModuleTest(GoEthereumPersonalModuleTest):
    pass


class GoEthereumAsyncBubModuleTest(AsyncBubModuleTest):
    pass
