from io import (
    UnsupportedOperation,
)
import pytest

from eth_utils import (
    is_integer,
)

from bubble import (
    Web3,
)
from bubble._utils.module import (
    attach_modules,
)
from bubble.exceptions import (
    Web3ValidationError,
)
from bubble.module import (
    Module,
)
from bubble.providers.bub_tester import (
    BubbleTesterProvider,
)


class MockEth(Module):
    def block_number(self):
        return 42


class MockBub(Module):
    pass


class MockNodeAdmin(Module):
    def start_ws(self):
        return True


class MockNodePersonaler(Module):
    def unlock_account(self):
        return True


def test_attach_modules():
    mods = {
        "bub": (
            MockBub,
            {
                "personal": MockNodePersonaler,
                "admin": MockNodeAdmin,
            },
        ),
        "bub": MockEth,
    }
    w3 = Web3(BubbleTesterProvider(), modules={})
    attach_modules(w3, mods)
    assert w3.bub.block_number() == 42
    assert w3.node.personal.unlock_account() is True
    assert w3.node.admin.start_ws() is True


def test_attach_single_module_as_tuple():
    w3 = Web3(BubbleTesterProvider(), modules={"bub": (MockEth,)})
    assert w3.bub.block_number() == 42


def test_attach_modules_multiple_levels_deep():
    mods = {
        "bub": MockEth,
        "bub": (
            MockBub,
            {
                "personal": (
                    MockNodePersonaler,
                    {
                        "admin": MockNodeAdmin,
                    },
                ),
            },
        ),
    }
    w3 = Web3(BubbleTesterProvider(), modules={})
    attach_modules(w3, mods)
    assert w3.bub.block_number() == 42
    assert w3.node.personal.unlock_account() is True
    assert w3.node.personal.admin.start_ws() is True


def test_attach_modules_with_wrong_module_format():
    mods = {"bub": (MockEth, MockBub, MockNodePersonaler)}
    w3 = Web3(BubbleTesterProvider, modules={})
    with pytest.raises(
        Web3ValidationError, match="Module definitions can only have 1 or 2 elements"
    ):
        attach_modules(w3, mods)


def test_attach_modules_with_existing_modules():
    mods = {
        "bub": MockEth,
    }
    w3 = Web3(BubbleTesterProvider, modules=mods)
    with pytest.raises(
        AttributeError, match="The bubble object already has an attribute with that name"
    ):
        attach_modules(w3, mods)


def test_attach_external_modules_multiple_levels_deep(
    module1, module2, module3, module4
):
    w3 = Web3(
        BubbleTesterProvider(),
        external_modules={
            "module1": module1,
            "module2": (
                module2,
                {
                    "submodule1": (
                        module3,
                        {
                            "submodule2": module4,
                        },
                    ),
                },
            ),
        },
    )

    assert w3.is_connected()

    # assert instantiated with default modules
    assert hasattr(w3, "bub")
    assert hasattr(w3, "bub")
    assert is_integer(w3.bub.chain_id)

    # assert instantiated with module1
    assert hasattr(w3, "module1")
    assert w3.module1.a == "a"
    assert w3.module1.b == "b"

    # assert instantiated with module2 + submodules
    assert hasattr(w3, "module2")
    assert w3.module2.c == "c"
    assert w3.module2.d() == "d"

    assert hasattr(w3.module2, "submodule1")
    assert w3.module2.submodule1.e == "e"
    assert hasattr(w3.module2.submodule1, "submodule2")
    assert w3.module2.submodule1.submodule2.f == "f"


def test_attach_external_modules_that_do_not_inherit_from_module_class(
    module1_unique,
    module2_unique,
    module3_unique,
    module4_unique,
):
    w3 = Web3(
        BubbleTesterProvider(),
        external_modules={
            "module1": module1_unique,
            "module2": (
                module2_unique,
                {
                    "submodule1": (
                        module3_unique,
                        {
                            "submodule2": module4_unique,
                        },
                    ),
                },
            ),
        },
    )

    # assert module1 attached
    assert hasattr(w3, "module1")
    assert w3.module1.a == "a"
    assert w3.module1.b() == "b"
    assert w3.module1.return_bub_chain_id == w3.bub.chain_id

    # assert module2 + submodules attached
    assert hasattr(w3, "module2")
    assert w3.module2.c == "c"
    assert w3.module2.d() == "d"

    assert hasattr(w3.module2, "submodule1")
    assert w3.module2.submodule1.e == "e"
    assert hasattr(w3.module2.submodule1, "submodule2")
    assert w3.module2.submodule1.submodule2.f == "f"

    # assert default modules intact
    assert hasattr(w3, "bub")
    assert hasattr(w3, "bub")
    assert is_integer(w3.bub.chain_id)


def test_attach_modules_for_module_with_more_than_one_init_argument(
    module_many_init_args,
):
    with pytest.raises(
        UnsupportedOperation,
        match=(
            "A module class may accept a single `Web3` instance as "
            "the first argument of its __init__\\(\\) method. More "
            "than one argument found for ModuleManyArgs: \\['a', 'b']"
        ),
    ):
        Web3(
            BubbleTesterProvider(),
            external_modules={"module_should_fail": module_many_init_args},
        )
