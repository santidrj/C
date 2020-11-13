import os
from math import ceil, log2, sqrt
from time import time

import Crypto.PublicKey.RSA as rsa
from gmpy2.gmpy2 import isqrt, mpz, t_mod, t_div


def calculate_k(n):
    return 2 ** (ceil(log2(n.bit_length())) - 1)


def factor(n):
    n = mpz(n)
    k = calculate_k(n)
    lower_n = n & ((2 ** k) - 1)
    mu_base = 2 ** (k // 2)
    max_lmd = int(lower_n - mu_base)
    i = 108

    for lmd in range(max_lmd, 0, -1):
        i -= 1
        remainder = t_mod(lower_n - lmd, mu_base)

        if remainder == 0:
            mu = t_div(lower_n - lmd, mu_base)

            print(f'lamda = {lmd}')
            print(f'mu = {mu}')

            div = 2 * 2 ** (-k // 2)
            try:
                b = int(sqrt((mu + sqrt(mu ** 2 - 4 * (lmd ** 2) * (2 ** -k))) // (2 * 2 ** (-k // 2))))
                a = int(lmd // b)

                p = a * mu_base + b
                q = b * mu_base + a
                if p * q == n:
                    return p, q
            except ValueError:
                pass

    return -1, -1


def main():
    input_path = os.path.join('../RSA_pseudo/santiago.del.rey_pubkeyRSA_pseudo.pem')
    with open(input_path, 'rb') as file:
        my_rsa_key = rsa.importKey(file.read())
        file.close()

    p, q = factor(my_rsa_key.n)
    assert p * q == my_rsa_key.n


if __name__ == '__main__':
    # main()
    n = 31356
    start = time()
    p, q = factor(n)
    print(f'Elapsed time: {time() - start}')

    print(f'p = {p}')
    print(f'q = {q}')
    assert p * q == n
