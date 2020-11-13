import os
from math import sqrt

import Crypto.PublicKey.RSA as rsa
from gmpy2.gmpy2 import mpz, ceil, log2, t_mod, t_div


def calculate_k(n):
    return 2 ** (ceil(log2(n.bit_length())) - 1)


def factor(n):
    n = mpz(n)
    k = calculate_k(n)
    lmd_base = mpz(2 ** k + 1)
    mu_base = mpz(2 ** (k // 2))
    lmd_max = mpz((n - mu_base) // lmd_base)

    for lmd in range(lmd_max, 0, -1):
        remainder = t_mod(n - lmd * lmd_base, mu_base)

        if remainder == 0:
            mu = t_div(n - lmd * lmd_base, mu_base)

            print(f'lamda = {lmd}')
            print(f'mu = {mu}')

            b = int(sqrt((mu + sqrt(mu ** 2 - 4 * (lmd ** 2))) // 2))
            a = int(lmd // b)

            return a * mu_base + b, b * mu_base + a

    return -1, -1


def main():
    input_path = os.path.join('../RSA_pseudo/santiago.del.rey_pubkeyRSA_pseudo.pem')
    with open(input_path, 'rb') as file:
        my_rsa_key = rsa.importKey(file.read())
        file.close()

    factor(my_rsa_key.n)


if __name__ == '__main__':
    main()
    # n = 31356
    # p, q = factor(n)
    #
    # print(f'p = {p}')
    # print(f'q = {q}')
    # assert p * q == n
