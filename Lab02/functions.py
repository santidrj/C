# %%
import math

import numpy as np
import time


def GF_product_p(a, b):
    """Realiza el producto de dos elementos en el cuerpo utilizando la definición en términos polinómicos.

    Args:
        a (integer): Un elemento del cuerpo representado por un entero entre 0 i 255.
        b (integer): Un elemento del cuerpo representado por un entero entre 0 i 255.

    Returns:
    integer: Un elemento del cuerpo representado por un enter entre 0 i 255.
    """

    if a == 0 or b == 0:
        return 0

    num_2 = np.binary_repr(b)
    partial_results = [0] * len(num_2)
    partial_results[0] = a

    grade = len(num_2) - 1
    result = a

    # Descomponemos el producto de mayor grado en productos n parciales
    for i in range(1, len(num_2)):
        bit7 = np.binary_repr(result, 8)[0]
        result = np.uint8(result << 1)

        # Si el bit 7 antes del shift era 1 entonces aplicamos el modulo
        if bit7 == '1':
            # result = result ^ 0x1D
            result = result ^ 0x1B  # AES

        # Almacenamos los resultados parciales
        partial_results[i] = result

    for i, bit in enumerate(num_2[1:], 1):
        if bit == '1':
            result = result ^ partial_results[grade - i]

    return result


def GF_es_generador(g):
    """Retorna cierto si g es generador del cuerpo.

    Args:
        g (integer): Elemento del cuerpo representado por un entero entre 0 i 255.

    Returns:
        boolean: True si g es generador del cuerpo, False si no lo es.
    """

    acc = 1
    for i in range(1, 256):
        acc = GF_product_p(acc, g)
        if acc == 1:
            return i == 255

    return False


def GF_tables():
    """Genera dos tablas (exponencial i logaritmo), una que en la posición i tenga a = g^i
    i otra que en la posición a tenga i tal que a = g^i. (g generador del cuerpo finito del cuerpo
    representado por el menor entero entre 0 i 255)
    """

    # g = 2
    g = 3  # AES
    acc = g
    t_exp = [1] * 256
    t_exp[1] = g
    t_log = [0] * 256
    t_log[g] = 1
    for i in range(2, 256):
        acc = GF_product_p(acc, g)
        t_exp[i] = acc
        t_log[acc] = i

    return t_exp, t_log


t_exp, t_log = GF_tables()


def GF_product_t(a, b):
    """Realiza el producto de dos elementos del cuerpo utilizando las tablas exponencial y logaritmo.

    Args:
        a (integer): Elemento del cuerpo representado por enteros entre 0 i 255.
        b (integer): Elemento del cuerpo representado por enteros entre 0 i 255.

    Returns:
        integer: Un elemento del cuerpo representado por un entero entre 0 i 255 que es el producto en el cuerpo de a i b.
    """
    if a == 0 or b == 0:
        return 0

    prod_i = (t_log[a] + t_log[b]) % 255
    prod = t_exp[prod_i]
    return prod


def GF_invers(a):
    """Retorna el inverso de a en el cuerpo.

    Args:
        a (integer): Elemento del cuerpo representado por enteros entre 0 i 255.

    Returns:
        integer: 0 si a=0x00, inverso de a en el cuerpo si a != 0x00 representado por un entero entre 1 i 255.
    """

    if a == 0:
        return 0
    # t_exp, t_log = GF_tables()
    return t_exp[255 - t_log[a]]


# %%
a = 0x82
v = [0x2B, 0x02, 0x03, 0x09, 0x0B, 0x0D, 0x0E]
n = 1000
for b in v:
    total_p_time = 0
    total_t_time = 0
    p_time = 0
    t_time = 0
    for i in range(n):
        p_init_time = time.time_ns()
        GF_product_p(a, b)
        p_time += (time.time_ns() - p_init_time)
        t_init_time = time.time_ns()
        GF_product_t(a, b)
        t_time += (time.time_ns() - t_init_time)
    total_p_time = p_time / n
    total_t_time = t_time / n
    print('Execution time of GF_product_p({},{}): {}'.format(a, b, total_p_time))
    print('Execution time of GF_product_t({},{}): {}\n'.format(a, b, total_t_time))

# %%
assert GF_invers(0) == 0

for i in range(1, 256):
    a = GF_product_p(i, GF_invers(i))
    assert a == 1

for i in range(256):
    for j in range(256):
        a = GF_product_p(i, j)
        b = GF_product_t(i, j)
        assert a == b

for i in range(256):
    for j in range(256):
        a = GF_product_p(i, j)
        b = GF_product_p(j, i)
        assert a == b

assert not GF_es_generador(0)

print('End')

# %%
print('Producto: ', GF_product_p(0x67, 0x06))
print('Inverso: ', GF_invers(0x04))

# %%
for g in range(256):
    if GF_es_generador(g):
        print(math.gcd(int(math.log(g)), 255))
