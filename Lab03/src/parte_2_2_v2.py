import os
from math import ceil, log2
from time import time

import Crypto.PublicKey.RSA as rsa
from gmpy2.gmpy2 import isqrt, mpz


def calculate_k(n):
    return 2 ** (ceil(log2(n.bit_length())) - 1)


def factor(n):
    k = calculate_k(n)
    upper_n = int(n >> k)
    lower_l = int(upper_n * 2 ** (k // 2 - 1))
    max_mu = lower_l * 2 ** (k // 2) + 2 ** (k // 2 - 1)

    for mu in range(max_mu, 0, -1):
        lmd = upper_n - (mu >> (k // 2))

        # print(f'lamda = {lmd}')
        # print(f'mu = {mu}')

        mu = mpz(mu)
        lmd = mpz(lmd)
        b = int(isqrt((mu + isqrt(mu ** 2 - 4 * (lmd ** 2))) // 2))
        a = int(lmd // b)

        p = a * 2 ** (k // 2) + b
        q = b * 2 ** (k // 2) + a

        if p * q == n:
            return p, q

    return -1, -1


def main():
    input_path = os.path.join('../RSA_pseudo/santiago.del.rey_pubkeyRSA_pseudo.pem')
    with open(input_path, 'rb') as file:
        my_rsa_key = rsa.importKey(file.read())
        file.close()

    p, q = factor(my_rsa_key.n)
    assert p * q == my_rsa_key.n


if __name__ == '__main__':
    main()
    # n = 31356
    # start = time()
    # p, q = factor(n)
    # print(f'Elapsed time: {time() - start}')
    #
    # print(f'p = {p}')
    # print(f'q = {q}')
    # assert p * q == n
