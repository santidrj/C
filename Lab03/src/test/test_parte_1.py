import pytest
from Lab03.src.rsa_key import rsa_key


@pytest.fixture
def rsa() -> rsa_key:
    return rsa_key(bits_modulo=512)


@pytest.fixture
def random_message() -> str:
    return 1231


def test_sign_equal_to_sign_slow(rsa, random_message):
    assert rsa.sign(random_message) == rsa.sign_slow(random_message), 'The signature is different while using sing_slow'
