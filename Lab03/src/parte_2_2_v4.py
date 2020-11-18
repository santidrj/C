import os

import Crypto.PublicKey.RSA as rsa
import numpy as np
from gmpy2.gmpy2 import ceil, log2

from sqrt_long_division import sqrt_long_division


def calculate_k(n):
    return 2 ** (ceil(log2(n.bit_length())) - 1)


def split_n(n):
    k = int(calculate_k(n))
    binary_n = np.binary_repr(n, 2 * k)[::-1]
    lower_rs = binary_n[0:k // 2]
    l = binary_n[k // 2: (3 * k // 2)]
    upper_rs = binary_n[3 * k // 2:]
    # OJO!! Los bits estan invertidos, hay que revertilos antes de pasarlos a enteros
    return k, upper_rs, l, lower_rs


def get_rs_1024(upper_rs, lower_rs):
    # Si suponemos que no ha habido overflow
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1024_overflow(upper_rs, lower_rs):
    # Si suponemos que ha habido overflow
    upper_rs = invert_bits(upper_rs)
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1025(upper_rs, lower_rs):
    # Si suponemos que no ha habido overflow
    if upper_rs[0] == '0':
        upper_rs = invert_bits(upper_rs)
    else:
        upper_rs = '0' + upper_rs[1:]
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def get_rs_1025_overflow(upper_rs, lower_rs):
    # Si suponemos que ha habido overflow
    upper_rs = upper_rs[0] + invert_bits(upper_rs[1:])
    rs = int((lower_rs + upper_rs)[::-1], 2)
    lmd = int((upper_rs + lower_rs)[::-1], 2)
    return rs, lmd


def invert_bits(upper_rs):
    u_rs = list(upper_rs)
    for idx, bit in enumerate(upper_rs):
        if bit == '0':
            u_rs[idx] = '1'
        else:
            u_rs[idx] = '0'
            break
    return ''.join(u_rs)


def calculate_r_s(rs, l, lmd):
    r = sqrt_long_division((-(lmd - l) + sqrt_long_division((lmd - l) ** 2 - 4 * (rs ** 2))) // 2)
    s = rs // r
    return r, s


def calculate_p_q(n, k, upper_rs, l, lower_rs):
    rs, lmd = get_rs_1024(upper_rs, lower_rs)
    p, q = get_p_q(k, int(l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1024_overflow(upper_rs, lower_rs)
    p, q = get_p_q(k, int('1' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1025(upper_rs, lower_rs)
    p, q = get_p_q(k, int('1' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    rs, lmd = get_rs_1025_overflow(upper_rs, lower_rs)
    p, q = get_p_q(k, int('10' + l[::-1], 2), rs, lmd)
    if n == p * q:
        return p, q

    return -1, -1


def get_p_q(k, l_int, rs, lmd):
    try:
        r, s = calculate_r_s(rs, l_int, lmd)
        p = int(np.binary_repr(r, k // 2) + np.binary_repr(s, k // 2), 2)
        q = int(np.binary_repr(s, k // 2) + np.binary_repr(r, k // 2), 2)
        return p, q
    except ValueError:
        return -1, -1


def main():
    input_path = os.path.join('../RSA_pseudo/santiago.del.rey_pubkeyRSA_pseudo.pem')
    with open(input_path, 'rb') as file:
        my_rsa_key = rsa.importKey(file.read())
        file.close()

    n = my_rsa_key.n
    k, upper_rs, l, lower_rs = split_n(n)
    p, q = calculate_p_q(n, k, upper_rs, l, lower_rs)
    assert n == (p * q)


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
