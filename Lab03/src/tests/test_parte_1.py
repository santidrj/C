import pytest

from block import block
from block_chain import block_chain
from rsa_key import rsa_key
from rsa_public_key import rsa_public_key
from transaction import transaction


@pytest.fixture
def rsa() -> rsa_key:
    return rsa_key(bits_modulo=512)


@pytest.fixture
def random_message() -> str:
    return 1231


@pytest.fixture
def trans(random_message, rsa) -> transaction:
    return transaction(random_message, rsa)


@pytest.fixture
def ablock(trans) -> block:
    return block().genesis(trans)


@pytest.fixture
def ablockchain(trans) -> block_chain:
    return block_chain(trans)


def test_sign_equal_to_sign_slow(rsa, random_message):
    assert rsa.sign(random_message) == rsa.sign_slow(random_message), 'The signature is different while using sing_slow'


def test_valid_rsa_public_key(rsa, random_message):
    public_key = rsa_public_key(rsa)
    signature = rsa.sign(random_message)
    assert public_key.verify(random_message, signature), \
        f"Message was {random_message} while decripted message " \
        f"was {pow(signature, public_key.publicExponent, public_key.modulus)}"


def test_valid_transaction(rsa, random_message):
    t = transaction(random_message, rsa)
    assert t.verify()


def test_genesis_is_valid_block(ablock):
    assert ablock.verify_block()


def test_valid_next_block(ablock, trans):
    assert ablock.next_block(trans).verify_block()


def test_invalid_next_block(ablock, trans):
    assert not ablock.next_wrong_block(trans).verify_block()


def test_valid_block_chain(ablockchain, trans):
    assert ablockchain.add_block(trans).add_block(trans).add_block(trans).verify(), \
        "The blockchain should be invalid but the verification says it's valid."


def test_invalid_block_chain(ablockchain, trans):
    valid, idx = ablockchain.add_block(trans).add_block(trans).add_wrong_block(trans).add_block(trans).verify()
    assert idx + 1 == 3, f"The position of the invalid block should be 3 but was {idx}."
